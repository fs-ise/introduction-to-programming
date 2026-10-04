"""Generate the student-facing index of files in the materials directory."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

import yaml


ROOT = Path(__file__).resolve().parents[1]
MATERIALS_DIR = ROOT / "materials"
OUTPUT_FILE = ROOT / "data" / "materials.generated.md"
GENERATED_VIEWERS_DIR = ROOT / "generated" / "materials"

# These artifacts are produced before the site render (see the publish workflow
# and the Makefile). Keep them in the overview even when the generator is run
# in a checkout where the ignored build output does not exist yet.
BUILT_MATERIALS = {Path("excel-cheat-sheet.pdf")}

CACHE_DIRECTORIES = {
    "__pycache__",
    ".cache",
    ".ipynb_checkpoints",
    "_book",
    "_freeze",
    "_site",
    "build",
    "cache",
    "dist",
    "node_modules",
}

TYPE_LABELS = {
    ".csv": "CSV file",
    ".docx": "Word document",
    ".html": "Web page",
    ".htm": "Web page",
    ".ipynb": "Jupyter notebook",
    ".pdf": "PDF",
    ".pptx": "PowerPoint presentation",
    ".qmd": "Web page",
    ".xls": "Excel workbook",
    ".xlsx": "Excel workbook",
    ".zip": "ZIP archive",
}


def casefold_path(path: Path) -> tuple[str, str]:
    """Return a deterministic, case-insensitive key for a relative path."""
    value = path.as_posix()
    return value.casefold(), value


def is_excluded_path(relative_path: Path) -> bool:
    """Return whether a path is implementation detail rather than course material."""
    for part in relative_path.parts:
        if part.startswith((".", "_")) or part.casefold() in CACHE_DIRECTORIES:
            return True

    filename = relative_path.name
    if filename == ".DS_Store" or filename.startswith(("_", "~$")):
        return True

    # Treat "solution" or "solutions" as a filename token. This covers both
    # *_solution.ext and common variants such as *_with_solutions.ext.
    return bool(re.search(r"(?:^|[\W_])solutions?(?:[\W_]|$)", relative_path.stem, re.I))


def publishable_files() -> list[Path]:
    """Find files that can be presented to students."""
    if not MATERIALS_DIR.exists():
        return []

    candidates: set[Path] = set(BUILT_MATERIALS)
    for path in MATERIALS_DIR.rglob("*"):
        if not path.is_file():
            continue
        relative_path = path.relative_to(MATERIALS_DIR)
        if is_excluded_path(relative_path):
            continue
        if path.suffix.casefold() in {".html", ".htm"} and path.with_suffix(".qmd").exists():
            continue
        candidates.add(relative_path)

    return sorted(candidates, key=casefold_path)


def qmd_title(path: Path) -> str | None:
    """Read a title from a QMD file's YAML front matter, if it has one."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        closing_line = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
        metadata = yaml.safe_load("\n".join(lines[1:closing_line])) or {}
    except (StopIteration, yaml.YAMLError):
        return None
    title = metadata.get("title") if isinstance(metadata, dict) else None
    return str(title).strip() if title is not None and str(title).strip() else None


def readable_label(path: Path) -> str:
    """Make a filename readable without hiding meaningful tokens or numbers."""
    words = re.sub(r"[_-]+", " ", path.stem).strip()
    return words[:1].upper() + words[1:] if words else path.name


def material_details(relative_path: Path) -> tuple[str, str, str]:
    """Return the label, link target, and type label for a material."""
    suffix = relative_path.suffix.casefold()
    label = (
        qmd_title(MATERIALS_DIR / relative_path) or readable_label(relative_path)
        if suffix == ".qmd"
        else readable_label(relative_path)
    )
    if suffix == ".py":
        target = Path("generated/materials") / relative_path.with_suffix(".html")
    else:
        target = Path("materials") / (
            relative_path.with_suffix(".html") if suffix == ".qmd" else relative_path
        )
    link = quote(target.as_posix(), safe="/")
    type_label = TYPE_LABELS.get(suffix, f"{suffix[1:].upper()} file" if suffix else "File")
    return label, link, type_label


def escape_table_text(value: str) -> str:
    """Escape text that would otherwise break a Markdown table cell."""
    return value.replace("|", "\\|").replace("\n", " ")


def section_title(directory: Path) -> str:
    """Create a student-facing heading for a relative directory."""
    if directory == Path("."):
        return "General materials"
    return " / ".join(readable_label(Path(part)) for part in directory.parts)


def generated_content(files: list[Path]) -> str:
    """Build the complete generated Markdown fragment."""
    lines = [
        "<!-- AUTO-GENERATED by scripts/generate_materials_overview.py. DO NOT EDIT. -->",
        "",
    ]
    if not files:
        lines.append("No student-facing materials are currently available.")
        return "\n".join(lines) + "\n"

    sections: dict[Path, list[Path]] = defaultdict(list)
    for path in files:
        sections[path.parent].append(path)

    for directory in sorted(sections, key=casefold_path):
        lines.extend([f"## {section_title(directory)}", "", "| Material | Type |", "|---|---|"])
        for path in sorted(sections[directory], key=casefold_path):
            label, link, type_label = material_details(path)
            lines.append(f"| [{escape_table_text(label)}]({link}) | {type_label} |")
        lines.append("")
    return "\n".join(lines)


def write_if_changed(path: Path, content: str) -> bool:
    """Write content only if it differs, preserving mtime for unchanged output."""
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def viewer_content(relative_path: Path) -> str:
    """Build a non-executing Quarto page that displays a Python source file."""
    source = (MATERIALS_DIR / relative_path).read_text(encoding="utf-8")
    # A longer fence keeps even source containing Markdown fences intact.
    backtick_runs = (len(match.group()) for match in re.finditer(r"`+", source))
    fence = "`" * max(3, max(backtick_runs, default=0) + 1)
    filename = relative_path.name.replace('"', r'\"')
    viewer_path = GENERATED_VIEWERS_DIR / relative_path.with_suffix(".qmd")
    source_path = MATERIALS_DIR / relative_path
    levels_to_root = len(viewer_path.relative_to(ROOT).parent.parts)
    download_target = (
        Path(*([".."] * levels_to_root)) / source_path.relative_to(ROOT)
    )

    return (
        "---\n"
        f"title: {json.dumps(relative_path.name)}\n"
        "code-copy: true\n"
        "execute:\n"
        "  enabled: false\n"
        "---\n\n"
        f"[Download source]({quote(download_target.as_posix(), safe='/')}){{.small}}\n\n"
        f'{fence}{{.python filename="{filename}"}}\n'
        f"{source}"
        f"{'' if source.endswith(chr(10)) else chr(10)}{fence}\n"
    )


def generate_viewers(files: list[Path]) -> tuple[int, int]:
    """Synchronize generated viewer sources and return (changed, total) counts."""
    python_files = [path for path in files if path.suffix.casefold() == ".py"]
    expected = {
        GENERATED_VIEWERS_DIR / path.with_suffix(".qmd") for path in python_files
    }
    changed = 0
    for stale_path in set(GENERATED_VIEWERS_DIR.rglob("*.qmd")) - expected:
        stale_path.unlink()
        changed += 1

    for relative_path in python_files:
        changed += write_if_changed(
            GENERATED_VIEWERS_DIR / relative_path.with_suffix(".qmd"),
            viewer_content(relative_path),
        )

    if GENERATED_VIEWERS_DIR.exists():
        for directory in sorted(GENERATED_VIEWERS_DIR.rglob("*"), reverse=True):
            if directory.is_dir() and not any(directory.iterdir()):
                directory.rmdir()
    return changed, len(python_files)


def main() -> None:
    """Generate the overview fragment."""
    files = publishable_files()
    changed = write_if_changed(OUTPUT_FILE, generated_content(files))
    viewer_changes, total = generate_viewers(files)
    status = "Updated" if changed else "Unchanged"
    print(f"{status}: {OUTPUT_FILE.relative_to(ROOT)}")
    print(
        f"Synchronized {total} Python viewer pages "
        f"({viewer_changes} changed) in {GENERATED_VIEWERS_DIR.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
