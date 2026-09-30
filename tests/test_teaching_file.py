from pathlib import Path
import re
import shutil
import subprocess

import pytest


ROOT = Path(__file__).parents[1]
SESSIONS = tuple(ROOT / "notes" / f"session_{number:02}.qmd" for number in range(4, 12))
SHORTCODE_PATTERN = re.compile(r"\{\{< teaching-file ([^ >]+\.py)(?: kind=\"([^\"]+)\")? >\}\}")
LEGACY_FILE_PATTERN = re.compile(
    r"::: \{\.teaching-file\}\s+.*?\[`([^`]+)`\]\(([^)]+)\).*?\s+:::", re.DOTALL
)


def test_teaching_file_shortcode_is_registered():
    manifest = (ROOT / "_extensions/teaching-file/_extension.yml").read_text()
    assert "shortcodes:" in manifest
    assert "teaching-file.lua" in manifest
    assert (ROOT / "_extensions/teaching-file/teaching-file.lua").is_file()


def test_notes_pdf_depends_on_teaching_file_extension():
    makefile = (ROOT / "Makefile").read_text()
    notes_dependencies = makefile.split("$(NOTES_PDF):", 1)[1].splitlines()[0]
    assert "_extensions/teaching-file/teaching-file.lua" in notes_dependencies
    assert "_extensions/teaching-file/_extension.yml" in notes_dependencies


def test_sessions_use_shortcode_for_python_teaching_files():
    for session_path in SESSIONS:
        session = session_path.read_text()
        assert not re.search(r"\{\{< include ../materials/session_\d+/[^ >]+\.py >\}\}", session)
        legacy_paths = [target for _label, target in LEGACY_FILE_PATTERN.findall(session)]
        assert not any(Path(path).suffix.lower() == ".py" for path in legacy_paths)

        shortcodes = SHORTCODE_PATTERN.findall(session)
        assert shortcodes, f"No Python teaching files found in {session_path.name}"
        for path, _kind in shortcodes:
            assert (session_path.parent / path).is_file(), path


def test_dataset_buttons_remain_separate_and_valid():
    dataset_buttons = []
    for session_path in SESSIONS:
        session = session_path.read_text()
        for label_path, target_path in LEGACY_FILE_PATTERN.findall(session):
            assert label_path == target_path
            assert Path(target_path).suffix.lower() in {".csv", ".xlsx"}
            assert (session_path.parent / target_path).is_file(), target_path
            dataset_buttons.append(target_path)

        assert all(
            Path(path).suffix.lower() == ".py"
            for path, _kind in SHORTCODE_PATTERN.findall(session)
        )

    assert dataset_buttons, "Expected the teaching notes to retain dataset download buttons"


def test_shortcode_builds_display_only_python_code_and_file_link():
    implementation = (ROOT / "_extensions/teaching-file/teaching-file.lua").read_text()
    assert "pandoc.CodeBlock" in implementation
    assert '{ "python" }, { eval = "false" }' in implementation
    assert "pandoc.Link" in implementation
    assert "io.open" in implementation


def test_shortcode_renders_default_and_explicit_kinds(tmp_path: Path):
    quarto = shutil.which("quarto")
    if quarto is None:
        pytest.skip("Quarto is not available")

    sample = tmp_path / "sample.py"
    sample.write_text('message = "teaching-file smoke test"\n', encoding="utf-8")
    source = tmp_path / "smoke.qmd"
    shortcode = ROOT / "_extensions/teaching-file/teaching-file.lua"
    source.write_text(
        f"---\nshortcodes:\n  - {shortcode.as_posix()}\n---\n\n"
        "{{< teaching-file sample.py >}}\n\n"
        '{{< teaching-file sample.py kind="demo" >}}\n\n'
        '{{< teaching-file sample.py kind="homework" >}}\n\n'
        '{{< teaching-file sample.py kind="homework-solution" >}}\n',
        encoding="utf-8",
    )

    subprocess.run(
        [quarto, "render", source.name, "--to", "html", "--output", "smoke.html"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=True,
    )

    rendered = (tmp_path / "smoke.html").read_text(encoding="utf-8")
    assert "In-class exercise" in rendered
    assert "In-class demo" in rendered
    assert "Homework" in rendered
    assert "Homework solution" in rendered
    assert "teaching-file smoke test" in rendered
