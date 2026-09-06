from pathlib import Path

from scripts.combine_notes import HTML_BR_FILTER, combine


def test_combine_preserves_html_line_breaks_and_configures_filter(tmp_path: Path) -> None:
    note = tmp_path / "note.qmd"
    source = (
        '---\ntitle: "Table note"\n---\n\n'
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
    assert HTML_BR_FILTER.is_absolute()
    assert note.read_text(encoding="utf-8") == source


def test_combined_pdf_configuration_and_page_breaks(tmp_path: Path) -> None:
    first = tmp_path / "session_01.qmd"
    first.write_text('---\ntitle: "Notes S-01/First"\n---\n\n## Topic one\n', encoding="utf-8")
    second = tmp_path / "session_02.qmd"
    second.write_text('---\ntitle: "Notes S-02/Second"\n---\n\n## Topic two\n', encoding="utf-8")
    output = tmp_path / "notes.qmd"

    combine(output, [first, second])

    combined = output.read_text(encoding="utf-8")
    assert "toc-depth: 1" in combined
    assert "papersize: a4" in combined
    assert "left=1.5cm" in combined
    assert "bottom=2.2cm" in combined
    assert "footskip=0.9cm" in combined
    assert r"\pretocmd{\subsection}{\clearpage}" in combined
    assert r"\usepackage{scrlayer-scrpage}" in combined
    assert "fancyhdr" not in combined
    assert r"\clearpairofpagestyles" in combined
    assert r"\ifoot[\mlbdfooterlabel]{\mlbdfooterlabel}" in combined
    assert r"\ofoot[\pagemark]{\pagemark}" in combined
    assert r"\pagestyle{scrheadings}" in combined
    assert r"\renewcommand{\mlbdfooterlabel}{MLBD Teaching Notes - Notes S-01/First}" in combined
    assert r"\renewcommand{\mlbdfooterlabel}{MLBD Teaching Notes - Notes S-02/Second}" in combined
    assert combined.count("\n\n\\newpage\n\n") == 2
    assert combined.index(r"MLBD Teaching Notes - Notes S-01/First") < combined.index(
        "# Notes S-01/First"
    )


def test_footer_title_is_latex_escaped(tmp_path: Path) -> None:
    note = tmp_path / "note.qmd"
    note.write_text(
        '---\ntitle: "50% R&D: #1_use of $x^{2}$, ~ and \\\\ paths"\n---\n\nText\n',
        encoding="utf-8",
    )
    output = tmp_path / "notes.qmd"

    combine(output, [note])

    combined = output.read_text(encoding="utf-8")
    assert (
        r"\renewcommand{\mlbdfooterlabel}{MLBD Teaching Notes - "
        r"50\% R\&D: \#1\_use of \$x\textasciicircum{}\{2\}\$, "
        r"\textasciitilde{} and \textbackslash{} paths}"
    ) in combined
