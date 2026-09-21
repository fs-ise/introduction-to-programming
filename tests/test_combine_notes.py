import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from scripts.combine_notes import (
    HTML_BR_FILTER,
    NEEDSPACE_SHORTCODE,
    TEACHING_BREAK_FILTER,
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
    assert f"  - {TEACHING_BREAK_FILTER.as_posix()}" in combined
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
    assert r"\usepackage{fvextra}" in combined
    assert r"\usepackage[skins]{tcolorbox}" in combined
    assert r"\tcbuselibrary{breakable}" in combined
    assert r"\newtcolorbox{teachingbreak}{%" in combined
    assert "borderline north={0.4pt}{0pt}{gray!45}" in combined
    assert "borderline south={0.4pt}{0pt}{gray!45}" in combined
    assert "halign=center" in combined
    assert r"fontupper=\bfseries" in combined
    # tcolorbox is unbreakable unless its `breakable` option is enabled.
    assert "        breakable," not in combined
    assert r"\AtBeginDocument{%" in combined
    assert r"\DefineVerbatimEnvironment{Highlighting}{Verbatim}{%" in combined
    assert r"commandchars=\\\{\},%" in combined
    assert r"\RecustomVerbatimEnvironment{verbatim}{Verbatim}{%" in combined
    assert combined.count("breaklines=true,%") == 2
    assert combined.count("breaknonspaceingroup=true,%") == 2
    assert combined.count("breakanywhere=true,%") == 2
    assert combined.count("breaksymbolleft={}%") == 2
    assert r"\pretocmd{\subsection}{\clearpage}" not in combined
    assert r"\usepackage{etoolbox}" not in combined
    assert r"\usepackage{scrlayer-scrpage}" in combined
    assert r"\DeclareTOCStyleEntry[" in combined
    assert (
        r"\newcommand{\notesTOCPageNumberBox}[1]{\makebox[8em][l]{#1}}"
        in combined
    )
    assert "pagenumberwidth=8em" in combined
    assert "rightindent=9em" in combined
    assert r"pagenumberbox=\notesTOCPageNumberBox" in combined
    assert r"\AfterTOCHead[toc]{%" in combined
    assert (
        r"\makebox[\dimexpr\linewidth-9em\relax][l]{\textbf{Section}}%"
        in combined
    )
    assert (
        r"\notesTOCPageNumberBox{\textbf{Pages start with}}\par" in combined
    )
    assert r"\textbf{Section}\hfill" not in combined
    assert "fancyhdr" not in combined
    assert r"\clearpairofpagestyles" in combined
    assert 'title: "Introduction to Programming Teaching Notes"' in combined
    assert (
        r"\ifoot[Introduction to Programming: Notes]"
        r"{Introduction to Programming: Notes}" in combined
    )
    assert r"\ofoot[\pagemark]{\pagemark}" in combined
    assert r"\pagestyle{scrheadings}" in combined
    assert "teachingnotesfooterlabel" not in combined
    assert (
        "Introduction to Programming Teaching Notes - Notes S-01/First"
        not in combined
    )
    assert (
        "Introduction to Programming Teaching Notes - Notes S-02/Second"
        not in combined
    )
    assert "MLBD" not in combined
    assert combined.count(r"\clearpage") == 2
    assert r"\renewcommand{\thepage}{Session-1/p\arabic{page}}" in combined
    assert r"\renewcommand{\thepage}{Session-2b/p\arabic{page}}" in combined
    assert combined.count(r"\setcounter{page}{1}") == 2
    assert "## Topic one" in combined
    assert "### Topic one detail" in combined
    assert "## Topic two" in combined
    assert combined.count("Introduction to Programming: Notes") == 2


def test_session_title_is_not_inserted_into_footer(tmp_path: Path) -> None:
    note = tmp_path / "note.qmd"
    note.write_text(
        '---\ntitle: "50% R&D: #1_use of $x^{2}$, ~ and \\\\ paths"\n'
        "session_id: session-03\n---\n\nText\n",
        encoding="utf-8",
    )
    output = tmp_path / "notes.qmd"

    combine(output, [note])

    combined = output.read_text(encoding="utf-8")
    assert "Introduction to Programming: Notes" in combined
    assert r"50\% R\&D" not in combined
    assert r"\renewcommand{\teachingnotesfooterlabel}" not in combined


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


def test_teaching_break_filter_targets_only_latex_teaching_breaks(
    tmp_path: Path,
) -> None:
    if shutil.which("pandoc") is not None:
        pandoc_command = ["pandoc"]
    elif shutil.which("quarto") is not None:
        # Quarto distributions include Pandoc even when it is not on PATH.
        pandoc_command = ["quarto", "pandoc"]
    else:
        pytest.skip("neither standalone nor Quarto-bundled Pandoc is available")

    source = (
        "::: {.teaching-break}\nBreak — 10 minutes\n:::\n\n"
        "::: {.other-callout}\nKeep me unchanged.\n:::\n"
    )
    markdown = tmp_path / "break.md"
    markdown.write_text(source, encoding="utf-8")

    latex = subprocess.run(
        [
            *pandoc_command,
            markdown.name,
            "--lua-filter",
            str(TEACHING_BREAK_FILTER),
            "-t",
            "latex",
        ],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    assert r"\begin{teachingbreak}" in latex
    assert "Break" in latex
    assert "10 minutes" in latex
    assert r"\end{teachingbreak}" in latex
    assert "Keep me unchanged." in latex

    html = subprocess.run(
        [
            *pandoc_command,
            markdown.name,
            "--lua-filter",
            str(TEACHING_BREAK_FILTER),
            "-t",
            "html",
        ],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    assert 'class="teaching-break"' in html
    assert "Break — 10 minutes" in html


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


def _pdf_tools_or_skip() -> None:
    required_commands = ["quarto", "pdftotext"]
    latex_commands = ["xelatex", "lualatex", "pdflatex", "tectonic"]
    missing = [
        command for command in required_commands if shutil.which(command) is None
    ]
    if not any(shutil.which(command) for command in latex_commands):
        missing.append("a LaTeX engine")
    if missing:
        pytest.skip(f"PDF rendering tools unavailable: {', '.join(missing)}")


def _render_pdf(combined: Path) -> tuple[str, Path]:
    rendered = subprocess.run(
        ["quarto", "render", combined.name, "--to", "pdf", "--output", "notes.pdf"],
        cwd=combined.parent,
        text=True,
        capture_output=True,
        check=False,
    )
    render_log = rendered.stdout + rendered.stderr
    assert rendered.returncode == 0, render_log
    return render_log, combined.with_name("notes.pdf")


def test_pdf_builds_with_quarto_callout_and_teaching_break(tmp_path: Path) -> None:
    _pdf_tools_or_skip()
    note = tmp_path / "note.qmd"
    note.write_text(
        '---\ntitle: "Callouts"\nsession_id: session-06\n---\n\n'
        "::: {.callout-note}\nA standard Quarto callout.\n:::\n\n"
        "::: {.teaching-break}\nBreak — 10 minutes\n:::\n",
        encoding="utf-8",
    )
    combined = tmp_path / "notes.qmd"
    combine(combined, [note])

    render_log, pdf = _render_pdf(combined)
    assert "I do not know the key '/tcb/breakable'" not in render_log

    extracted = subprocess.run(
        ["pdftotext", pdf.name, "-"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    assert "A standard Quarto callout." in extracted
    assert "Break — 10 minutes" in extracted


def test_long_highlighted_code_wraps_inside_pdf_text_area(tmp_path: Path) -> None:
    _pdf_tools_or_skip()
    long_token = "https://example.invalid/" + "unbroken-path-segment-" * 14
    note = tmp_path / "note.qmd"
    note.write_text(
        '---\ntitle: "Code wrapping"\nsession_id: session-04\n---\n\n'
        "```python\n"
        'short_value = "unchanged"\n'
        f'long_value = "{long_token}"\n'
        "```\n",
        encoding="utf-8",
    )
    combined = tmp_path / "notes.qmd"
    combine(combined, [note])

    render_log, pdf = _render_pdf(combined)
    assert "Overfull \\hbox" not in render_log

    text = subprocess.run(
        ["pdftotext", "-layout", pdf.name, "-"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    assert long_token in "".join(text.split())
    assert 'short_value = "unchanged"' in text

    bbox_xml = subprocess.run(
        ["pdftotext", "-bbox-layout", pdf.name, "-"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    root = ET.fromstring(bbox_xml)
    pages = [element for element in root.iter() if element.tag.endswith("page")]
    assert pages
    page_width = float(pages[0].attrib["width"])
    code_words = [
        word
        for word in root.iter()
        if word.tag.endswith("word")
        and (word.text or "").strip()
        and (
            "example.invalid" in (word.text or "")
            or "unbroken-path" in (word.text or "")
        )
    ]
    assert code_words
    assert len({round(float(word.attrib["yMin"]), 1) for word in code_words}) > 1
    # The document has 1.5 cm margins; tolerate a few points of glyph overhang.
    assert max(float(word.attrib["xMax"]) for word in code_words) < page_width - 35


def test_pdf_with_only_plain_fenced_code_builds(tmp_path: Path) -> None:
    _pdf_tools_or_skip()
    long_token = "plain_" * 80
    note = tmp_path / "note.qmd"
    note.write_text(
        '---\ntitle: "Plain code"\nsession_id: session-05\n---\n\n'
        "```\n"
        f"{long_token}\n"
        "```\n",
        encoding="utf-8",
    )
    combined = tmp_path / "notes.qmd"
    combine(combined, [note])

    render_log, pdf = _render_pdf(combined)
    assert "Overfull \\hbox" not in render_log
    extracted = subprocess.run(
        ["pdftotext", pdf.name, "-"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    assert long_token in "".join(extracted.split())
