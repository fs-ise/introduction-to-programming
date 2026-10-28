from pathlib import Path

import pytest

from scripts.teaching_progress import load_tracks, render_coverage_forms, teaching_files

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def test_tracks_are_loaded_from_course_yaml(tmp_path: Path) -> None:
    config = tmp_path / "course.yml"
    config.write_text("tracks:\n  - A1\n  - A2\n", encoding="utf-8")

    assert load_tracks(config) == ("A1", "A2")


@pytest.mark.parametrize(
    "yaml_text",
    [
        "tracks: []\n",
        "tracks:\n  - E3\n  - E3\n",
        "tracks:\n  - E3\n  - ''\n",
    ],
)
def test_track_configuration_must_be_nonempty_and_unique(
    tmp_path: Path, yaml_text: str
) -> None:
    config = tmp_path / "course.yml"
    config.write_text(yaml_text, encoding="utf-8")

    with pytest.raises(ValueError):
        load_tracks(config)


def test_inventory_reads_all_shortcode_occurrences_from_sessions_06_to_11() -> None:
    sources = [
        (5, '{{< teaching-file ../materials/session_05/ignored.py >}}'),
        (
            6,
            """{{< teaching-file ../materials/session_05/homework.py >}}
{{< teaching-file ../materials/session_06/example.py kind="demo" >}}
{{< teaching-file ../materials/session_06/example.py >}}
::: {.teaching-file}
[data.csv](../materials/data/data.csv)""",
        ),
        (11, "{{< teaching-file ../materials/session_11/final.py kind='homework' >}}"),
        (12, "{{< teaching-file ../materials/session_12/ignored.py >}}"),
    ]

    files = teaching_files(sources)

    assert [(item.session, Path(item.path).name) for item in files] == [
        (6, "homework.py"),
        (6, "example.py"),
        (6, "example.py"),
        (11, "final.py"),
    ]


def test_coverage_forms_have_completed_box_wide_note_and_full_gridlines() -> None:
    form = render_coverage_forms(
        [
            (6, '{{< teaching-file ../materials/session_05/homework.py >}}'),
            (6, '{{< teaching-file ../materials/session_06/example.py kind="demo" >}}'),
            (7, '{{< teaching-file ../materials/session_07/another.py >}}'),
        ],
        ("E3", "E4"),
    )

    assert "## Session 06 - Track E3" in form
    assert "## Session 06 - Track E4" in form
    assert "## Session 07 - Track E3" in form
    assert "## Session 07 - Track E4" in form
    assert "**Shared with tutor:** $\\square$" in form
    assert (
        r"\begin{tabularx}{\linewidth}{|>{\arraybackslash}p{7cm}|"
        r">{\centering\arraybackslash}p{2.5cm}|>{\arraybackslash}X|}\hline"
    ) in form
    assert (
        r"\textbf{Exercise} & \textbf{Completed} & "
        r"\textbf{To be discussed in tutorial sessions}"
    ) in form
    assert form.count(r"\newpage") == 1
    assert (
        form.index("## Session 06 - Track E4")
        < form.index(r"\newpage")
        < form.index("## Session 07 - Track E3")
        < form.index("## Session 07 - Track E4")
    )
    assert r"\renewcommand{\arraystretch}{1.25}" in form
    assert r"\rule{0pt}{7mm}" in form
    assert "homework.py" in form
    assert "example.py" in form
    assert "(demo)" not in form
    assert "N = not covered" not in form
    assert "|---" not in form
    form_lines = form.splitlines()
    for heading, needspace in (
        ("## Session 06 - Track E3", r"\Needspace{16\baselineskip}"),
        ("## Session 06 - Track E4", r"\Needspace{16\baselineskip}"),
        ("## Session 07 - Track E3", r"\Needspace{14\baselineskip}"),
        ("## Session 07 - Track E4", r"\Needspace{14\baselineskip}"),
    ):
        heading_index = form_lines.index(heading)
        assert form_lines[heading_index - 4] == "```{=latex}"
        assert form_lines[heading_index - 3] == needspace
        assert form_lines[heading_index - 2] == "```"
        table_end = form_lines.index(r"\end{tabularx}\endgroup", heading_index)
        tutor_checkbox = form_lines.index(r"**Shared with tutor:** $\square$", heading_index)
        assert table_end < tutor_checkbox
    # Three file checkboxes per track and one tutor-sharing box per track/session.
    assert form.count(r"$\square$") == 3 * 2 + 2 * 2


def test_empty_inventory_does_not_render_coverage_forms() -> None:
    assert render_coverage_forms([(5, "{{< teaching-file old.py >}}")], ("E3",)) == ""


def test_sessions_06_to_11_point_to_forms_after_groups() -> None:
    for session in range(6, 12):
        source = (
            REPOSITORY_ROOT / "notes" / f"session_{session:02d}.qmd"
        ).read_text(encoding="utf-8")
        assert (
            "See the Python solution coverage forms after **Groups** at the beginning "
            "of the printed teaching notes."
        ) in source
