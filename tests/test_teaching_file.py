from pathlib import Path
import re
import shutil
import subprocess

import pytest


ROOT = Path(__file__).parents[1]
SESSION = ROOT / "notes" / "session_04.qmd"
PYTHON_FILES = (
    "Spydertest.py",
    "CircleArea1.py",
    "FutureValue.py",
    "countries.py",
    "insurance.py",
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


def test_session_04_uses_shortcode_for_each_python_file():
    session = SESSION.read_text()
    assert not re.search(r"include ../materials/session_04/[^ >]+\.py", session)
    for filename in PYTHON_FILES:
        path = f"../materials/session_04/{filename}"
        assert session.count(f"{{{{< teaching-file {path}") == 1
        assert (ROOT / "materials/session_04" / filename).is_file()


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
        '{{< teaching-file sample.py kind="demo" >}}\n',
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
    assert "teaching-file smoke test" in rendered
