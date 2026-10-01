from pathlib import Path
import re
import shutil
import subprocess

import pytest


ROOT = Path(__file__).parents[1]
SESSIONS = tuple(ROOT / "notes" / f"session_{number:02}.qmd" for number in range(4, 12))
SHORTCODE_PATTERN = re.compile(
    r"\{\{<\s*teaching-file\s+([^\s>]+\.py)([^>]*)>\}\}"
)
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


def test_session_07_interactive_formula_homework_mapping():
    session = (ROOT / "notes/session_07.qmd").read_text()

    for filename in ("Traveltime.py", "Fuel.py", "AnnuityLoan1.py"):
        assert re.search(
            rf"teaching-file ../materials/session_07/{filename} kind=\"homework\"",
            session,
        )

    for filename in ("CircleArea2.py", "Currency.py", "Distance.py"):
        assert re.search(
            rf"teaching-file ../materials/session_07/{filename}\s*>", session
        )


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
    assert "quarto.Callout" in implementation
    assert "title = title" in implementation
    assert "content = { code }" in implementation


def test_shortcode_renders_callout_options_and_explicit_kinds(tmp_path: Path):
    quarto = shutil.which("quarto")
    if quarto is None:
        pytest.skip("Quarto is not available")

    sample = tmp_path / "sample.py"
    sample.write_text(
        'raise RuntimeError("teaching-file code must not be evaluated")\n',
        encoding="utf-8",
    )
    source = tmp_path / "smoke.qmd"
    shortcode = ROOT / "_extensions/teaching-file/teaching-file.lua"
    source.write_text(
        f"---\nshortcodes:\n  - {shortcode.as_posix()}\n---\n\n"
        "{{< teaching-file sample.py >}}\n\n"
        '{{< teaching-file sample.py kind="homework" callout="TrUe" >}}\n\n'
        '{{< teaching-file sample.py callout="false" >}}\n\n'
        '{{< teaching-file sample.py kind="demo" callout="FALSE" >}}\n',
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
    assert rendered.count("In-class exercise") == 2
    assert "In-class demo" in rendered
    assert rendered.count("Homework") == 1
    assert rendered.count('href="sample.py"') == 4
    assert rendered.count("teaching-file code must not be evaluated") == 4
    callouts = re.findall(
        r'class="(?=[^"]*\bcallout\b)(?=[^"]*\bcallout-tip\b)[^"]*"',
        rendered,
    )
    # Only the default and callout="TrUe" instances are Quarto callouts. The
    # two false instances remain an unboxed download row and code block.
    assert len(callouts) == 2

    titles = re.findall(
        r'<div class="[^"]*\bcallout-title-container\b[^"]*">(.*?)</div>',
        rendered,
        re.DOTALL,
    )
    assert len(titles) == 2
    assert "In-class exercise" in titles[0]
    assert "Homework" in titles[1]
    assert all("sample.py" in title for title in titles)
    assert all('href="sample.py"' in title for title in titles)

    # Callout titles replace the download row rather than duplicating it in
    # the body; only the two callout=false instances retain this standalone row.
    teaching_rows = re.findall(
        r'class="(?=[^"]*\bteaching-file\b)[^"]*"', rendered
    )
    assert len(teaching_rows) == 2


def test_shortcode_rejects_invalid_callout_value(tmp_path: Path):
    quarto = shutil.which("quarto")
    if quarto is None:
        pytest.skip("Quarto is not available")

    (tmp_path / "sample.py").write_text("pass\n", encoding="utf-8")
    shortcode = ROOT / "_extensions/teaching-file/teaching-file.lua"
    source = tmp_path / "invalid.qmd"
    source.write_text(
        f"---\nshortcodes:\n  - {shortcode.as_posix()}\n---\n\n"
        '{{< teaching-file sample.py callout="sometimes" >}}\n',
        encoding="utf-8",
    )

    result = subprocess.run(
        [quarto, "render", source.name, "--to", "html"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
    )

    assert result.returncode != 0
    assert "callout must be 'true' or 'false'" in result.stdout + result.stderr
