from pathlib import Path

from scripts.combine_notes import combine


def test_combined_pdf_configuration_and_page_breaks(tmp_path: Path) -> None:
    first = tmp_path / "session_01.qmd"
    first.write_text('---\ntitle: "Notes S-01/First"\n---\n\n## Topic one\n', encoding="utf-8")
    second = tmp_path / "session_02.qmd"
    second.write_text('---\ntitle: "Notes S-02/Second"\n---\n\n## Topic two\n', encoding="utf-8")
    output = tmp_path / "notes.qmd"

    combine(output, [first, second])

    combined = output.read_text(encoding="utf-8")
    assert "toc-depth: 1" in combined
    assert "margin=1.5cm" in combined
    assert r"\pretocmd{\subsection}{\clearpage}" in combined
    assert r"\renewcommand{\sectionmark}" in combined
    assert r"\fancyhead[L]{MLBD Teaching Notes}" in combined
    assert r"\fancyfoot[C]{Page \thepage}" in combined
    assert combined.count("\n\n\\newpage\n\n# Notes") == 2
