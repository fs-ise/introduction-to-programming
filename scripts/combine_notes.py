"""Assemble session notes into one Quarto source document."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

HTML_BR_FILTER = Path(__file__).resolve().with_name("html_br_to_linebreak.lua")
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
COURSE_CONFIG = REPOSITORY_ROOT / "course.yml"
NEEDSPACE_SHORTCODE = REPOSITORY_ROOT / "_extensions" / "needspace" / "needspace.lua"


def session_page_prefix(session_id: object, path: Path) -> str:
    """Return a display prefix derived from a note's session ID."""
    if not isinstance(session_id, str) or not session_id:
        raise ValueError(f"{path} has no session_id in its YAML front matter")

    match = re.fullmatch(r"session-(\d+)([a-z]*)", session_id)
    if match is None:
        raise ValueError(
            f"{path} has invalid session_id {session_id!r}; "
            "expected session-N with an optional lowercase-letter suffix"
        )

    number, suffix = match.groups()
    return f"Session-{int(number)}{suffix}"


def read_note(path: Path) -> tuple[str, str, str]:
    """Return the title, body, and page prefix of a front-matter QMD file."""
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path} does not start with YAML front matter")

    try:
        yaml_end = next(
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == "---"
        )
    except StopIteration as error:
        raise ValueError(f"{path} has unterminated YAML front matter") from error

    metadata = yaml.safe_load("\n".join(lines[1:yaml_end])) or {}
    title = metadata.get("title")
    if not isinstance(title, str) or not title:
        raise ValueError(f"{path} has no title in its YAML front matter")

    page_prefix = session_page_prefix(metadata.get("session_id"), path)
    return title, "\n".join(lines[yaml_end + 1 :]).strip(), page_prefix


def read_checklist(path: Path) -> tuple[str, str]:
    """Return the title and body of a heading-led reusable QMD fragment."""
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError(f"{path} does not start with a level-1 heading")

    title = lines[0][2:].strip()
    if not title:
        raise ValueError(f"{path} has an empty level-1 heading")
    return title, "\n".join(lines[1:]).strip()


def read_course_title() -> str:
    """Return the course title from the repository configuration."""
    config = yaml.safe_load(COURSE_CONFIG.read_text(encoding="utf-8")) or {}
    title = config.get("course", {}).get("title")
    if not isinstance(title, str) or not title:
        raise ValueError(f"{COURSE_CONFIG} has no course.title")
    return title


def combine(output: Path, inputs: list[Path], checklist: Path | None = None) -> None:
    """Combine note files into one PDF-oriented Quarto source."""
    teaching_notes_title = f"{read_course_title()} Teaching Notes"
    sections: list[str] = []

    sources = []
    if checklist is not None:
        title, body = read_checklist(checklist)
        sources.append((title, body, "Checklist"))
    sources.extend(read_note(path) for path in inputs)

    for title, body, page_prefix in sources:
        sections.append(f"""```{{=latex}}
\\clearpage
\\renewcommand{{\\thepage}}{{{page_prefix}/p\\arabic{{page}}}}
\\setcounter{{page}}{{1}}
```

# {title}

{body}""")

    front_matter = f"""---
title: "{teaching_notes_title}"
papersize: a4
filters:
  - {HTML_BR_FILTER.as_posix()}
shortcodes:
  - {NEEDSPACE_SHORTCODE.as_posix()}
format:
  pdf:
    toc: true
    toc-depth: 1
    number-sections: false
    geometry:
      - left=1.5cm
      - right=1.5cm
      - top=1.5cm
      - bottom=2.2cm
      - includefoot
      - footskip=0.9cm
    header-includes: |
      \\usepackage{{scrlayer-scrpage}}
      \\usepackage{{needspace}}
      \\usepackage{{fvextra}}

      % Pandoc defines Highlighting in its template, after header-includes has
      % been processed.  Delay the customization so that it replaces Pandoc's
      % definition, and configure its plain verbatim environment separately.
      \\AtBeginDocument{{%
        \\DefineVerbatimEnvironment{{Highlighting}}{{Verbatim}}{{%
          commandchars=\\\\\\{{\\}},%
          breaklines=true,%
          breaknonspaceingroup=true,%
          breakanywhere=true,%
          breaksymbolleft={{}}%
        }}%
        \\RecustomVerbatimEnvironment{{verbatim}}{{Verbatim}}{{%
          breaklines=true,%
          breaknonspaceingroup=true,%
          breakanywhere=true,%
          breaksymbolleft={{}}%
        }}%
      }}

      \\DeclareTOCStyleEntry[
        pagenumberwidth=8em,
        rightindent=9em
      ]{{tocline}}{{section}}

      \\AfterTOCHead[toc]{{%
        \\noindent\\textbf{{Section}}\\hfill\\textbf{{Pages start with}}\\par
        \\smallskip
      }}

      % The optional arguments apply the same footer to plain.scrheadings,
      % which KOMA uses for pages that would otherwise have a plain style.
      \\clearpairofpagestyles
      \\ifoot[Introduction to Programming: Notes]{{Introduction to Programming: Notes}}
      \\ofoot[\\pagemark]{{\\pagemark}}
      \\pagestyle{{scrheadings}}
---
"""

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        front_matter + "\n\n".join(sections) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checklist", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("inputs", nargs="+", type=Path)
    arguments = parser.parse_args()
    combine(arguments.output, arguments.inputs, arguments.checklist)


if __name__ == "__main__":
    main()
