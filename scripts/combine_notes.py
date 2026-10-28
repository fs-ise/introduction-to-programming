"""Assemble session notes into one Quarto source document."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

HTML_BR_FILTER = Path(__file__).resolve().with_name("html_br_to_linebreak.lua")
TEACHING_BREAK_FILTER = Path(__file__).resolve().with_name("teaching_break.lua")
CENTER_CAPTIONLESS_IMAGES_FILTER = (
    Path(__file__).resolve().with_name("center_captionless_images.lua")
)
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
COURSE_CONFIG = REPOSITORY_ROOT / "course.yml"
NEEDSPACE_SHORTCODE = REPOSITORY_ROOT / "_extensions" / "needspace" / "needspace.lua"
TEACHING_FILE_SHORTCODE = (
    REPOSITORY_ROOT / "_extensions" / "teaching-file" / "teaching-file.lua"
)
QRCODE_SHORTCODE = REPOSITORY_ROOT / "_extensions" / "jmbuhr" / "qrcode" / "qrcode.lua"
MERMAID_CONFIG = REPOSITORY_ROOT / "assets" / "mermaid-init.json"
SLIDE_RANGE = re.compile(r"\s*(\d+)\s*(?:[-–—]\s*(\d+))?\s*")


def mermaid_init_directive() -> str:
    """Return the PDF renderer's directive from the shared Mermaid config."""
    config = json.loads(MERMAID_CONFIG.read_text(encoding="utf-8"))
    return f"%%{{init: {json.dumps(config, indent=2)}}}%%"


ACADEMIC_MERMAID_INIT = mermaid_init_directive()


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


def _read_note_source(source: str, path: Path) -> tuple[str, str, str, str]:
    """Return a note's title, body, page prefix, and validated slide range."""
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
    if not isinstance(metadata, dict):
        raise ValueError(f"{path} YAML front matter must be a mapping")
    title = metadata.get("title")
    if not isinstance(title, str) or not title:
        raise ValueError(f"{path} has no title in its YAML front matter")

    page_prefix = session_page_prefix(metadata.get("session_id"), path)
    if "slide_range" not in metadata:
        raise ValueError(f"{path} has no slide_range in its YAML front matter")
    slide_range = normalize_slide_range(metadata["slide_range"], path)
    return title, "\n".join(lines[yaml_end + 1 :]).strip(), page_prefix, slide_range


def read_note(path: Path) -> tuple[str, str, str]:
    """Return the title, body, and page prefix of a front-matter QMD file."""
    title, body, page_prefix, _ = _read_note_source(
        path.read_text(encoding="utf-8"), path
    )
    return title, body, page_prefix


def normalize_slide_range(value: object, path: Path) -> str:
    """Validate and format a slide range from YAML front matter."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"{path} has invalid slide_range {value!r}; "
            "expected a string in the form N or N–M"
        )

    match = SLIDE_RANGE.fullmatch(value)
    if match is None:
        raise ValueError(f"{path} has invalid slide_range {value!r}; expected N or N–M")

    start = int(match.group(1))
    end = int(match.group(2) or start)
    if start < 1:
        raise ValueError(f"{path} has invalid slide_range {value!r}; slides start at 1")
    if end < start:
        raise ValueError(
            f"{path} has invalid slide_range {value!r}; end precedes start"
        )
    return str(start) if start == end else f"{start}–{end}"


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

    sources: list[tuple[str, str, str, str | None]] = []
    if groups is not None:
        title, body = read_groups(groups)
        sources.append((title, remove_rooms_from_groups(body), "Groups", None))
    if checklist is not None:
        title, body = read_checklist(checklist)
        sources.append((title, body, "Checklist", None))

    for path in inputs:
        source = path.read_text(encoding="utf-8")
        title, body, page_prefix, slide_range = _read_note_source(source, path)
        sources.append((title, body, page_prefix, slide_range))

    for title, body, page_prefix, slide_range in sources:
        latex_slide_range = (
            slide_range.replace("–", "--")
            if slide_range is not None
            else r"\textemdash{}"
        )
        sections.append(f"""```{{=latex}}
\\clearpage
\\renewcommand{{\\thepage}}{{{page_prefix}/p\\arabic{{page}}}}
\\setcounter{{page}}{{1}}
```

# {title} \\protect\\notesTOCSlides{{{latex_slide_range}}}

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

      % Reserve separate columns for slide ranges and custom page labels.
      % KOMA positions the page-number box at \\linewidth-\\rightindent;
      % retain a 1em gap after the combined 14em box.
      \\newcommand{{\\notesTOCCurrentSlides}}{{\\textemdash}}
      \\newcommand{{\\notesTOCSlides}}[1]{{\\gdef\\notesTOCCurrentSlides{{#1}}}}
      \\newcommand{{\\notesTOCPageNumberBox}}[1]{{%
        \\makebox[6em][c]{{\\notesTOCCurrentSlides}}%
        \\makebox[8em][l]{{#1}}%
      }}
      \\newcommand{{\\notesTOCHeaderBox}}[1]{{%
        \\makebox[6em][c]{{\\textbf{{Slides}}}}%
        \\makebox[8em][l]{{#1}}%
      }}
      \\DeclareTOCStyleEntry[
        pagenumberwidth=14em,
        rightindent=15em,
        pagenumberbox=\\notesTOCPageNumberBox
      ]{{tocline}}{{section}}

      \\AfterTOCHead[toc]{{%
        \\noindent
        \\makebox[\\dimexpr\\linewidth-15em\\relax][l]{{\\textbf{{Section}}}}%
        \\hspace*{{1em}}%
        \\notesTOCHeaderBox{{\\textbf{{Pages start with}}}}\\par
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
    combine(
        arguments.output,
        arguments.inputs,
        checklist=arguments.checklist,
        groups=arguments.groups,
    )


if __name__ == "__main__":
    main()
