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
    assert "title = make_title" in implementation
    assert "content = { make_code(contents) }" in implementation


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


def _render_shortcode(
    tmp_path: Path,
    source_lines: list[str],
    output_format: str,
    options: str = "",
) -> str:
    """Render one teaching-file shortcode and return the generated document."""
    quarto = shutil.which("quarto")
    if quarto is None:
        pytest.skip("Quarto is not available")

    (tmp_path / "sample.py").write_text(
        "\n".join(source_lines) + "\n", encoding="utf-8"
    )
    shortcode = ROOT / "_extensions/teaching-file/teaching-file.lua"
    source = tmp_path / "split.qmd"
    source.write_text(
        f"---\nshortcodes:\n  - {shortcode.as_posix()}\n---\n\n"
        f"{{{{< teaching-file sample.py {options} >}}}}\n",
        encoding="utf-8",
    )
    suffix = "tex" if output_format == "latex" else output_format
    output = tmp_path / f"split.{suffix}"
    subprocess.run(
        [quarto, "render", source.name, "--to", output_format, "--output", output.name],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=True,
    )
    return output.read_text(encoding="utf-8")


def _numbered_source(line_count: int) -> list[str]:
    # Deliberately omit blank lines so chunk boundaries are deterministic.
    return [f"source_line_{number:03} = {number}" for number in range(1, line_count + 1)]


def test_short_file_is_one_latex_callout(tmp_path: Path):
    rendered = _render_shortcode(tmp_path, _numbered_source(8), "latex")
    assert rendered.count("In-class exercise") == 1
    assert "continued from previous page" not in rendered


def test_long_file_remains_one_html_callout(tmp_path: Path):
    rendered = _render_shortcode(
        tmp_path, _numbered_source(30), "html", 'max-lines="10"'
    )
    assert rendered.count("In-class exercise") == 1
    assert "continued from previous page" not in rendered
    assert rendered.count("source_line_001") == 1
    assert rendered.count("source_line_030") == 1


def test_long_file_splits_in_latex_without_changing_source_order(tmp_path: Path):
    source_lines = _numbered_source(23)
    rendered = _render_shortcode(
        tmp_path, source_lines, "latex", 'split="true" max-lines="10"'
    )

    assert rendered.count("In-class exercise") == 3
    assert rendered.count("continued from previous page") == 2
    assert rendered.count(r"\newpage{}") == 2
    first_title = rendered.index("In-class exercise")
    assert r"\Needspace{" in rendered[:first_title]
    assert r"\newpage{}" not in rendered[:first_title]

    positions = []
    for line in source_lines:
        # LaTeX escaping and syntax-highlighting commands can occur within a
        # line, so the unique numeric suffix is the stable rendered marker.
        marker = line.split("_")[2].split()[0]
        assert rendered.count(marker) == 1
        positions.append(rendered.index(marker))
    assert positions == sorted(positions)


def test_split_false_disables_latex_splitting(tmp_path: Path):
    rendered = _render_shortcode(
        tmp_path,
        _numbered_source(25),
        "latex",
        'split="false" max-lines="10"',
    )
    assert rendered.count("In-class exercise") == 1
    assert "continued from previous page" not in rendered


def test_custom_max_lines_is_honored(tmp_path: Path):
    rendered = _render_shortcode(
        tmp_path, _numbered_source(13), "latex", 'max-lines="5"'
    )
    assert rendered.count("In-class exercise") == 3
    assert rendered.count("continued from previous page") == 2


def test_long_lines_consume_more_of_latex_chunk_budget(tmp_path: Path):
    short_render = _render_shortcode(
        tmp_path, [f"value_{number} = {number}" for number in range(4)], "latex",
        'max-lines="4"',
    )
    long_render = _render_shortcode(
        tmp_path,
        [f'long_{number} = "{"x" * 150}"' for number in range(4)],
        "latex",
        'max-lines="4"',
    )

    assert short_render.count("In-class exercise") == 1
    assert long_render.count("In-class exercise") == 4
    assert long_render.count("continued from previous page") == 3


@pytest.mark.parametrize(
    ("options", "message"),
    [
        ('split="sometimes"', "split must be 'auto', 'true', or 'false'"),
        ('max-lines="many"', "max-lines must be a positive integer"),
        ('max-lines="0"', "max-lines must be a positive integer"),
        ('max-lines="-2"', "max-lines must be a positive integer"),
    ],
)
def test_invalid_split_options_fail_clearly(
    tmp_path: Path, options: str, message: str
):
    quarto = shutil.which("quarto")
    if quarto is None:
        pytest.skip("Quarto is not available")
    (tmp_path / "sample.py").write_text("pass\n", encoding="utf-8")
    shortcode = ROOT / "_extensions/teaching-file/teaching-file.lua"
    (tmp_path / "invalid.qmd").write_text(
        f"---\nshortcodes:\n  - {shortcode.as_posix()}\n---\n\n"
        f"{{{{< teaching-file sample.py {options} >}}}}\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [quarto, "render", "invalid.qmd", "--to", "html"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert message in result.stdout + result.stderr


def test_homes_florida_pdf_callout_stays_inside_page(tmp_path: Path):
    """Regression test for the visibly overflowing Session 7 callout."""
    quarto = shutil.which("quarto")
    if quarto is None:
        pytest.skip("Quarto is not available")
    fitz = pytest.importorskip("fitz", reason="PyMuPDF is needed for PDF geometry")

    source_file = ROOT / "materials/session_07/Homes_Florida.py"
    (tmp_path / source_file.name).write_bytes(source_file.read_bytes())
    shortcode = ROOT / "_extensions/teaching-file/teaching-file.lua"
    (tmp_path / "regression.qmd").write_text(
        "---\nformat: pdf\nheader-includes: |\n"
        "  \\usepackage{needspace}\nshortcodes:\n"
        f"  - {shortcode.as_posix()}\n---\n\n"
        f"{{{{< teaching-file {source_file.name} >}}}}\n",
        encoding="utf-8",
    )
    subprocess.run(
        [quarto, "render", "regression.qmd", "--to", "pdf"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=True,
    )

    document = fitz.open(tmp_path / "regression.pdf")
    pages = [page for page in document if source_file.name in page.get_text()]
    assert len(pages) >= 2, "The long file should produce continuation callouts"
    assert "import pandas as pd" in " ".join(pages[0].get_text().split())
    assert all(
        "continued from previous page" in " ".join(page.get_text().split())
        for page in pages[1:]
    )
    for page in pages:
        # Filled drawing paths include the callout and code backgrounds. Every
        # such rectangle must be wholly contained by the physical MediaBox.
        filled_rectangles = [
            drawing["rect"] for drawing in page.get_drawings() if drawing["fill"]
        ]
        assert filled_rectangles
        assert all(page.rect.contains(rect) for rect in filled_rectangles)
