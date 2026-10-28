"""Build printable solution-coverage forms from the Python teaching notes."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

FIRST_SESSION = 6
LAST_SESSION = 11

TEACHING_FILE_SHORTCODE = re.compile(
    r"\{\{<\s*teaching-file\s+(?P<path>[^\s>]+)[^>]*>\}\}"
)

@dataclass(frozen=True)
class TeachingFile:
    session: int
    path: str


def load_tracks(course_config: Path) -> tuple[str, ...]:
    """Read and validate configured track names from the course YAML file."""
    config = yaml.safe_load(course_config.read_text(encoding="utf-8")) or {}
    if not isinstance(config, dict):
        raise TypeError(f"{course_config} must contain a YAML mapping")
    tracks = config.get("tracks")
    if not isinstance(tracks, list) or not tracks:
        raise ValueError(f"{course_config} must define a non-empty tracks list")
    if any(not isinstance(track, str) or not track.strip() for track in tracks):
        raise ValueError(f"{course_config} tracks must contain non-empty strings")
    if len(set(tracks)) != len(tracks):
        raise ValueError(f"{course_config} tracks must be unique")
    return tuple(tracks)


def teaching_files(session_sources: list[tuple[int, str]]) -> list[TeachingFile]:
    """Return teaching-file shortcode occurrences from Sessions 06–11."""
    files: list[TeachingFile] = []
    for session, source in session_sources:
        if not FIRST_SESSION <= session <= LAST_SESSION:
            continue

        for match in TEACHING_FILE_SHORTCODE.finditer(source):
            files.append(TeachingFile(session=session, path=match.group("path")))
    return files


def _latex_escape(value: str) -> str:
    """Escape text embedded in the printable LaTeX table."""
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in value)


def _session_form(
    session: int,
    track: str,
    files: list[TeachingFile],
) -> str:
    needed_lines = len(files) * 2 + 12
    lines = [
        "```{=latex}",
        rf"\Needspace{{{needed_lines}\baselineskip}}",
        "```",
        "",
        f"## Session {session:02d} - Track {_latex_escape(track)}",
        "",
        r"\begingroup\renewcommand{\arraystretch}{1.25}",
        r"\begin{tabularx}{\linewidth}{|p{5.5cm}|p{3cm}|X|}\hline",
        r"\textbf{Teaching file} & \textbf{Completed} & \textbf{Note} \\ \hline",
    ]
    for teaching_file in files:
        filename = _latex_escape(Path(teaching_file.path).name)
        lines.append(
            rf"\texttt{{{filename}}} & $\square$ & \rule{{0pt}}{{7mm}} \\ \hline"
        )
    lines.extend(
        [
            r"\end{tabularx}\endgroup",
            "",
            r"**Shared with tutor:** $\square$",
        ]
    )
    return "\n".join(lines)


def render_coverage_forms(
    session_sources: list[tuple[int, str]], tracks: tuple[str, ...]
) -> str:
    """Render handwritten coverage forms for configured tracks by session."""
    files = teaching_files(session_sources)
    if not files:
        return ""

    by_session: dict[int, list[TeachingFile]] = {}
    for teaching_file in files:
        by_session.setdefault(teaching_file.session, []).append(teaching_file)

    sections = [
        (
            "Check each file when completed and use the Note column for broader "
            "comments. At the end of the session, share the update with the "
            "appropriate tutor and tick the track's sharing checkbox."
        ),
    ]
    for session in sorted(by_session):
        for track in tracks:
            sections.extend([_session_form(session, track, by_session[session]), ""])
    return "\n\n".join(sections).strip()
