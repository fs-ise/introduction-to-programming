from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MERMAID_CSS = REPOSITORY_ROOT / "assets" / "mermaid.css"


def test_html_mermaid_palette_uses_light_structural_fills() -> None:
    css = MERMAID_CSS.read_text(encoding="utf-8")

    assert "--mermaid-bg-color: #ffffff" in css
    assert "--mermaid-edge-color: #777777" in css
    assert "--mermaid-node-bg-color: #ffffff" in css
    assert "--mermaid-node-fg-color: #999999" in css
    assert "--mermaid-label-fg-color: #222222" in css
    assert "--mermaid-fg-color--lighter: #d5d5d5" in css
    assert "--mermaid-fg-color--lightest: #f7f7f7" in css
    assert "--mermaid-font-family: inherit" in css


def test_mermaid_css_loads_last_in_each_html_output() -> None:
    root = yaml.safe_load((REPOSITORY_ROOT / "_quarto.yml").read_text())
    notes = yaml.safe_load((REPOSITORY_ROOT / "notes" / "_metadata.yml").read_text())
    exercises = yaml.safe_load(
        (REPOSITORY_ROOT / "exercises" / "_quarto.yml").read_text()
    )
    slides = yaml.safe_load(
        (REPOSITORY_ROOT / "slides" / "_metadata.yml").read_text()
    )

    assert root["format"]["html"]["css"][-1] == "assets/mermaid.css"
    assert notes["format"]["html"]["css"][-1] == "../assets/mermaid.css"
    assert exercises["format"]["html"]["css"][-1] == "../assets/mermaid.css"
    assert slides["format"]["revealjs"]["css"][-1] == "../assets/mermaid.css"
