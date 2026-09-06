"""Assemble session notes into one Quarto source document."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def escape_latex(value: str) -> str:
    """Escape arbitrary text for use as a LaTeX command argument."""
    replacements = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "$": r"\$",
        "&": r"\&",
        "#": r"\#",
        "_": r"\_",
        "%": r"\%",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(character, character) for character in value)


def read_note(path: Path) -> tuple[str, str]:
    """Return the title and body of a QMD file with YAML front matter."""
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

    return title, "\n".join(lines[yaml_end + 1 :]).strip()


def combine(output: Path, inputs: list[Path]) -> None:
    """Combine note files into one PDF-oriented Quarto source."""
    sections: list[str] = []

    for path in inputs:
        title, body = read_note(path)
        footer_label = escape_latex(f"MLBD Teaching Notes - {title}")
        sections.append(
            f"""```{{=latex}}
\\renewcommand{{\\mlbdfooterlabel}}{{{footer_label}}}
```

# {title}

{body}"""
        )

    front_matter = r"""---
title: "MLBD Teaching Notes"
papersize: a4
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
      \usepackage{scrlayer-scrpage}
      \usepackage{etoolbox}

      % The optional arguments apply the same footer to plain.scrheadings,
      % which KOMA uses for pages that would otherwise have a plain style.
      \newcommand{\mlbdfooterlabel}{MLBD Teaching Notes}
      \clearpairofpagestyles
      \ifoot[\mlbdfooterlabel]{\mlbdfooterlabel}
      \ofoot[\pagemark]{\pagemark}
      \pagestyle{scrheadings}

      % Start every level-2 heading on a new page.
      \pretocmd{\subsection}{\clearpage}{}{}
---
"""

    page_break = "\n\n\\newpage\n\n"

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        front_matter + page_break + page_break.join(sections) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("inputs", nargs="+", type=Path)
    arguments = parser.parse_args()
    combine(arguments.output, arguments.inputs)


if __name__ == "__main__":
    main()
