"""Assemble session notes into one Quarto source document."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

HTML_BR_FILTER = Path(__file__).resolve().with_name("html_br_to_linebreak.lua")
TEACHING_BREAK_FILTER = Path(__file__).resolve().with_name("teaching_break.lua")
CENTER_CAPTIONLESS_IMAGES_FILTER = Path(__file__).resolve().with_name(
    "center_captionless_images.lua"
)
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
COURSE_CONFIG = REPOSITORY_ROOT / "course.yml"
NEEDSPACE_SHORTCODE = REPOSITORY_ROOT / "_extensions" / "needspace" / "needspace.lua"
TEACHING_FILE_SHORTCODE = (
    REPOSITORY_ROOT / "_extensions" / "teaching-file" / "teaching-file.lua"
)
QRCODE_SHORTCODE = (
    REPOSITORY_ROOT / "_extensions" / "jmbuhr" / "qrcode" / "qrcode.lua"
)

ACADEMIC_MERMAID_INIT = """%%{init: {
  "theme": "base",
  "themeVariables": {
    "background": "#ffffff",
    "primaryColor": "#ffffff",
    "primaryTextColor": "#222222",
    "primaryBorderColor": "#999999",
    "lineColor": "#777777",
    "secondaryColor": "#ffffff",
    "tertiaryColor": "#f7f7f7",
    "clusterBkg": "#f7f7f7",
    "clusterBorder": "#cccccc",
    "edgeLabelBackground": "#ffffff"
  },
  "flowchart": {
    "curve": "linear"
  }
}}%%"""


def inject_academic_mermaid_config(markdown: str) -> str:
    """Inject the static-rendering theme into unconfigured Mermaid fences."""
    lines = markdown.splitlines(keepends=True)
    opening = re.compile(
        r"^(?P<indent>[ \t]*)(?P<fence>`{3,}|~{3,})"
        r"\{mermaid(?:[ ,][^}]*)?\}(?:[ \t].*)?[\r\n]*$"
    )
    explicit_init = re.compile(r"^[ \t]*%%\{[ \t]*init[ \t]*:", re.IGNORECASE)
    cell_option = re.compile(r"^[ \t]*%%\|")
    transformed: list[str] = []
    index = 0

    while index < len(lines):
        match = opening.match(lines[index])
        if match is None:
            transformed.append(lines[index])
            index += 1
            continue

        fence = match.group("fence")
        closing = re.compile(
            rf"^[ \t]*{re.escape(fence[0])}{{{len(fence)},}}[ \t]*[\r\n]*$"
        )
        end = index + 1
        while end < len(lines) and closing.match(lines[end]) is None:
            end += 1

        # An unterminated fence is left untouched rather than consuming the
        # remainder of the generated document as Mermaid source.
        if end == len(lines):
            transformed.extend(lines[index:])
            break

        block = lines[index : end + 1]
        if any(explicit_init.match(line) for line in block[1:-1]):
            transformed.extend(block)
            index = end + 1
            continue

        insert_at = 1
        while insert_at < len(block) - 1 and cell_option.match(block[insert_at]):
            insert_at += 1

        newline = "\r\n" if lines[index].endswith("\r\n") else "\n"
        indent = match.group("indent")
        directive = "".join(
            indent + line + newline for line in ACADEMIC_MERMAID_INIT.splitlines()
        )
        transformed.extend(block[:insert_at])
        transformed.append(directive)
        transformed.extend(block[insert_at:])
        index = end + 1

    return "".join(transformed)


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


def read_groups(path: Path) -> tuple[str, str]:
    """Return the title and body of the shared Groups section fragment."""
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()
    if not lines or not lines[0].startswith("## "):
        raise ValueError(f"{path} does not start with a level-2 heading")

    title = lines[0][3:].strip()
    if not title:
        raise ValueError(f"{path} has an empty level-2 heading")
    return title, "\n".join(lines[1:]).strip()


def remove_rooms_from_groups(body: str) -> str:
    """Remove trailing room segments from cells in a Groups Markdown table."""
    room_segment = re.compile(r"<br\s*/?>[ \t]*Room:[^|]*?([ \t]*)$")
    lines = []
    for line in body.splitlines():
        if line.lstrip().startswith("|") and line.rstrip().endswith("|"):
            cells = line.split("|")
            cells = [room_segment.sub(r"\1", cell) for cell in cells]
            line = "|".join(cells)
        lines.append(line)
    return "\n".join(lines)


def read_course_title() -> str:
    """Return the course title from the repository configuration."""
    config = yaml.safe_load(COURSE_CONFIG.read_text(encoding="utf-8")) or {}
    title = config.get("course", {}).get("title")
    if not isinstance(title, str) or not title:
        raise ValueError(f"{COURSE_CONFIG} has no course.title")
    return title


def combine(
    output: Path,
    inputs: list[Path],
    checklist: Path | None = None,
    groups: Path | None = None,
) -> None:
    """Combine note files into one PDF-oriented Quarto source."""
    teaching_notes_title = f"{read_course_title()} Teaching Notes"
    sections: list[str] = []

    sources = []
    if groups is not None:
        title, body = read_groups(groups)
        sources.append((title, remove_rooms_from_groups(body), "Groups"))
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
  - {TEACHING_BREAK_FILTER.as_posix()}
  - {CENTER_CAPTIONLESS_IMAGES_FILTER.as_posix()}
shortcodes:
  - {NEEDSPACE_SHORTCODE.as_posix()}
  - {TEACHING_FILE_SHORTCODE.as_posix()}
  - {QRCODE_SHORTCODE.as_posix()}
format:
  pdf:
    mermaid-format: png
    fig-align: center
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
      \\usepackage{{xcolor}}
      \\usepackage{{qrcode}}
      \\usepackage[skins]{{tcolorbox}}
      \\tcbuselibrary{{breakable}}

      % A restrained, unbreakable callout for breaks in the teaching schedule.
      \\newtcolorbox{{teachingbreak}}{{%
        enhanced,
        colback=gray!8,
        frame hidden,
        boxrule=0pt,
        borderline north={{0.4pt}}{{0pt}}{{gray!45}},
        borderline south={{0.4pt}}{{0pt}}{{gray!45}},
        arc=1.5mm,
        outer arc=1.5mm,
        left=5mm,
        right=5mm,
        top=3mm,
        bottom=3mm,
        before skip=6mm,
        after skip=6mm,
        halign=center,
        fontupper=\\bfseries
      }}

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

      % KOMA positions the page-number box at \\linewidth-\\rightindent.  Keep
      % the box width and trailing space explicit so the heading can use the
      % very same column boundary.
      \\newcommand{{\\notesTOCPageNumberBox}}[1]{{\\makebox[8em][l]{{#1}}}}
      \\DeclareTOCStyleEntry[
        pagenumberwidth=8em,
        rightindent=9em,
        pagenumberbox=\\notesTOCPageNumberBox
      ]{{tocline}}{{section}}

      \\AfterTOCHead[toc]{{%
        \\noindent
        \\makebox[\\dimexpr\\linewidth-9em\\relax][l]{{\\textbf{{Section}}}}%
        \\notesTOCPageNumberBox{{\\textbf{{Pages start with}}}}\\par
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
    combined = front_matter + "\n\n".join(sections) + "\n"
    output.write_text(inject_academic_mermaid_config(combined), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--groups", type=Path)
    parser.add_argument("--checklist", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("inputs", nargs="+", type=Path)
    arguments = parser.parse_args()
    combine(arguments.output, arguments.inputs, arguments.checklist, arguments.groups)


if __name__ == "__main__":
    main()
