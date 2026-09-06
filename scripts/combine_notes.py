"""Assemble session notes into one Quarto source document."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def read_note(path: Path) -> tuple[str, str]:
    """Return the title and body of a QMD file with YAML front matter."""
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path} does not start with YAML front matter")

    try:
        yaml_end = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"
        )
    except StopIteration as error:
        raise ValueError(f"{path} has unterminated YAML front matter") from error

    metadata = yaml.safe_load("\n".join(lines[1:yaml_end])) or {}
    title = metadata.get("title")
    if not isinstance(title, str) or not title:
        raise ValueError(f"{path} has no title in its YAML front matter")

    return title, "\n".join(lines[yaml_end + 1 :]).strip()


def combine(output: Path, inputs: list[Path]) -> None:
    sections = []
    for path in inputs:
        title, body = read_note(path)
        sections.append(f"# {title}\n\n{body}")

    front_matter = """---
title: "Teaching Notes"
format:
  pdf:
    toc: true
    number-sections: false
---"""
    page_break = "\n\n\\newpage\n\n"
    output.write_text(
        front_matter + "\n\n" + page_break.join(sections) + "\n",
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
