import json
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MERMAID_CSS = REPOSITORY_ROOT / "assets" / "mermaid.css"
MERMAID_CONFIG = REPOSITORY_ROOT / "assets" / "mermaid-init.json"


def test_html_mermaid_palette_uses_light_structural_fills() -> None:
    css = MERMAID_CSS.read_text(encoding="utf-8")

    assert "--mermaid-bg-color: #ffffff" in css
    assert "--mermaid-edge-color: #555555" in css
    assert "--mermaid-node-bg-color: #ffffff" in css
    assert "--mermaid-node-fg-color: #555555" in css
    assert "--mermaid-label-fg-color: #222222" in css
    assert "--mermaid-fg-color--lighter: #777777" in css
    assert "--mermaid-fg-color--lightest: #f7f7f7" in css
    assert "--mermaid-font-family: inherit" in css


def test_shared_mermaid_config_uses_native_neutral_hand_drawn_look() -> None:
    config = json.loads(MERMAID_CONFIG.read_text(encoding="utf-8"))

    assert config["theme"] == "base"
    assert config["look"] == "handDrawn"
    assert config["handDrawnSeed"] != 0
    assert config["themeCSS"] == ".nodeLabel { min-width: 300px; }"
    assert config["themeVariables"]["primaryColor"] == "#ffffff"
    assert config["themeVariables"]["primaryTextColor"] == "#222222"
    assert config["themeVariables"]["lineColor"] == "#555555"
    assert config["themeVariables"]["clusterBkg"] == "#f7f7f7"
    assert config["themeVariables"]["edgeLabelBackground"] == "#ffffff"
    # Keep flowchart sizing on Mermaid's supported spacing and padding options.
    assert config["flowchart"] == {
        "curve": "linear",
        "rankSpacing": 30,
        "nodeSpacing": 40,
        "padding": 8,
        "diagramPadding": 5,
    }


def test_session_05_uses_shared_mermaid_config() -> None:
    source = (REPOSITORY_ROOT / "notes" / "session_05.qmd").read_text(
        encoding="utf-8"
    )

    assert "%%{init:" not in source
    assert "Selecting data" in source
    assert "Modifying and sorting data" in source


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
    assert root["filters"] == ["scripts/mermaid_style.lua"]
    assert exercises["filters"] == ["../scripts/mermaid_style.lua"]
