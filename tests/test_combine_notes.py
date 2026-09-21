import shutil
import subprocess
from pathlib import Path

import pytest

from scripts.combine_notes import (
    HTML_BR_FILTER,
    NEEDSPACE_SHORTCODE,
    combine,
    session_page_prefix,
)

NEEDSPACE_EXTENSION = Path(__file__).resolve().parents[1] / "_extensions" / "needspace"


def test_combine_preserves_html_line_breaks_and_configures_filter(
    tmp_path: Path,
) -> None:
    note = tmp_path / "note.qmd"
    source = (
        '---\ntitle: "Table note"\nsession_id: session-01\n---\n\n'
        "| Time | Material |\n"
        "|---|---|\n"
        "| 35–55 min | Slides 7–10<br>Slides 7 and 10<br />Exercise |\n"
    )
    note.write_text(source, encoding="utf-8")
    output = tmp_path / "notes.qmd"

    combine(output, [note])

    combined = output.read_text(encoding="utf-8")
    assert "Slides 7–10<br>Slides 7 and 10<br />Exercise" in combined
    assert f"filters:\n  - {HTML_BR_FILTER.as_posix()}" in combined
    assert f"shortcodes:\n  - {NEEDSPACE_SHORTCODE.as_posix()}" in combined
    assert HTML_BR_FILTER.is_absolute()
    assert NEEDSPACE_SHORTCODE.is_absolute()
    assert note.read_text(encoding="utf-8") == source


def test_combined_pdf_configuration_and_page_breaks(tmp_path: Path) -> None:
    first = tmp_path / "session_01.qmd"
    first.write_text(
        '---\ntitle: "Notes S-01/First"\nsession_id: session-01\n---\n\n'
        "## Topic one\n\n### Topic one detail\n",
        encoding="utf-8",
    )
    second = tmp_path / "session_02.qmd"
    second.write_text(
        '---\ntitle: "Notes S-02/Second"\nsession_id: session-02b\n---\n\n'
        "## Topic two\n",
        encoding="utf-8",
    )
    output = tmp_path / "notes.qmd"

    combine(output, [first, second])

    combined = output.read_text(encoding="utf-8")
    assert "toc-depth: 1" in combined
    assert "papersize: a4" in combined
    assert "left=1.5cm" in combined
    assert "bottom=2.2cm" in combined
    assert "footskip=0.9cm" in combined
    assert r"\usepackage{needspace}" in combined
    assert r"\pretocmd{\subsection}{\clearpage}" not in combined
    assert r"\usepackage{etoolbox}" not in combined
    assert r"\usepackage{scrlayer-scrpage}" in combined
    assert r"\DeclareTOCStyleEntry[" in combined
    assert "pagenumberwidth=8em" in combined
    assert "rightindent=9em" in combined
    assert r"\AfterTOCHead[toc]{%" in combined
    assert r"\textbf{Section}\hfill\textbf{Pages start with}" in combined
    assert "fancyhdr" not in combined
    assert r"\clearpairofpagestyles" in combined
    assert 'title: "Introduction to Programming Teaching Notes"' in combined
    assert r"\ifoot[\teachingnotesfooterlabel]{\teachingnotesfooterlabel}" in combined
    assert r"\ofoot[\pagemark]{\pagemark}" in combined
    assert r"\pagestyle{scrheadings}" in combined
    assert (
        r"\renewcommand{\teachingnotesfooterlabel}"
        r"{Introduction to Programming Teaching Notes - Notes S-01/First}" in combined
    )
    assert (
        r"\renewcommand{\teachingnotesfooterlabel}"
        r"{Introduction to Programming Teaching Notes - Notes S-02/Second}" in combined
    )
    assert "MLBD" not in combined
    assert combined.count(r"\clearpage") == 2
    assert r"\renewcommand{\thepage}{Session-1/p\arabic{page}}" in combined
    assert r"\renewcommand{\thepage}{Session-2b/p\arabic{page}}" in combined
    assert combined.count(r"\setcounter{page}{1}") == 2
    assert "## Topic one" in combined
    assert "### Topic one detail" in combined
    assert "## Topic two" in combined
    assert combined.index(
        r"Introduction to Programming Teaching Notes - Notes S-01/First"
    ) < combined.index("# Notes S-01/First")


def test_footer_title_is_latex_escaped(tmp_path: Path) -> None:
    note = tmp_path / "note.qmd"
    note.write_text(
        '---\ntitle: "50% R&D: #1_use of $x^{2}$, ~ and \\\\ paths"\n'
        "session_id: session-03\n---\n\nText\n",
        encoding="utf-8",
    )
    output = tmp_path / "notes.qmd"

    combine(output, [note])

    combined = output.read_text(encoding="utf-8")
    assert (
        r"\renewcommand{\teachingnotesfooterlabel}"
        r"{Introduction to Programming Teaching Notes - "
        r"50\% R\&D: \#1\_use of \$x\textasciicircum{}\{2\}\$, "
        r"\textasciitilde{} and \textbackslash{} paths}"
    ) in combined


def test_checklist_appears_before_sessions(tmp_path: Path) -> None:
    checklist = tmp_path / "teaching_checklist.qmd"
    checklist.write_text(
        "# Teaching checklist\n\n## Room setup\n\n- [ ] Check projector.\n",
        encoding="utf-8",
    )
    note = tmp_path / "session_01.qmd"
    note.write_text(
        '---\ntitle: "Session 01"\nsession_id: session-01\n---\n\n## Topic\n',
        encoding="utf-8",
    )
    output = tmp_path / "notes.qmd"

    combine(output, [note], checklist)

    combined = output.read_text(encoding="utf-8")
    assert combined.index("# Teaching checklist") < combined.index("# Session 01")
    assert "- [ ] Check projector." in combined
    assert combined.count(r"\clearpage") == 2
    checklist_page = r"\renewcommand{\thepage}{Checklist/p\arabic{page}}"
    session_page = r"\renewcommand{\thepage}{Session-1/p\arabic{page}}"
    assert checklist_page in combined
    assert session_page in combined
    assert combined.index(checklist_page) < combined.index("# Teaching checklist")
    assert combined.index(session_page) < combined.index("# Session 01")


@pytest.mark.parametrize(
    ("session_id", "expected"),
    [
        ("session-01", "Session-1"),
        ("session-11", "Session-11"),
        ("session-003a", "Session-3a"),
    ],
)
def test_session_page_prefix(session_id: str, expected: str, tmp_path: Path) -> None:
    assert session_page_prefix(session_id, tmp_path / "note.qmd") == expected


@pytest.mark.parametrize("session_id", [None, "", "03", "session-three", "session-2-A"])
def test_invalid_session_page_prefix_is_informative(
    session_id: object, tmp_path: Path
) -> None:
    path = tmp_path / "note.qmd"
    with pytest.raises(ValueError) as error:
        session_page_prefix(session_id, path)

    assert str(path) in str(error.value)
    assert "session_id" in str(error.value)


def test_needspace_extension_supports_pdf_and_ignores_html() -> None:
    manifest = (NEEDSPACE_EXTENSION / "_extension.yml").read_text(encoding="utf-8")
    shortcode = (NEEDSPACE_EXTENSION / "needspace.lua").read_text(encoding="utf-8")

    assert "shortcodes:\n    - needspace.lua" in manifest
    assert 'quarto.doc.is_format("pdf")' in shortcode
    assert 'return pandoc.Str("")' in shortcode
    assert 'args[1] or "5"' in shortcode
    assert r"\\Needspace{%s\\baselineskip}" in shortcode


def test_generated_document_renders_needspace_shortcode(tmp_path: Path) -> None:
    required_commands = ["quarto", "pdftotext"]
    latex_commands = ["xelatex", "lualatex", "pdflatex", "tectonic"]
    missing = [
        command for command in required_commands if shutil.which(command) is None
    ]
    if not any(shutil.which(command) for command in latex_commands):
        missing.append("a LaTeX engine")
    if missing:
        pytest.skip(f"PDF rendering tools unavailable: {', '.join(missing)}")

    note = tmp_path / "note.qmd"
    note.write_text(
        '---\ntitle: "Shortcode integration"\nsession_id: session-01\n---\n\n'
        "Before the pagination directive.\n\n"
        "{{< needspace 3 >}}\n\n"
        "After the pagination directive.\n",
        encoding="utf-8",
    )
    combined = tmp_path / "notes.qmd"
    combine(combined, [note])

    rendered = subprocess.run(
        ["quarto", "render", combined.name, "--to", "pdf", "--output", "notes.pdf"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )
    render_log = rendered.stdout + rendered.stderr
    assert rendered.returncode == 0, render_log
    assert "Shortcode 'needspace' not found" not in render_log

    extracted = subprocess.run(
        ["pdftotext", "notes.pdf", "-"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    assert "Before the pagination directive." in extracted
    assert "After the pagination directive." in extracted
    assert "needspace" not in extracted.lower()
