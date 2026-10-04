from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import generate_materials_overview


class MaterialsOverviewTest(unittest.TestCase):
    def test_generated_content_includes_excel_cheat_sheet(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            materials_dir = Path(tmpdir)

            with patch.object(generate_materials_overview, "MATERIALS_DIR", materials_dir):
                content = generate_materials_overview.generated_content(
                    generate_materials_overview.publishable_files()
                )

        self.assertIn(
            "[Excel cheat sheet](materials/excel-cheat-sheet.pdf) | PDF",
            content,
        )

    def test_viewer_uses_nested_disabled_execute_configuration(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            materials_dir = root / "materials"
            viewers_dir = root / "generated" / "materials"
            source_path = Path("session_04/example.py")
            (materials_dir / source_path).parent.mkdir(parents=True)
            (materials_dir / source_path).write_text("print('example')\n", encoding="utf-8")

            with (
                patch.object(generate_materials_overview, "ROOT", root),
                patch.object(generate_materials_overview, "MATERIALS_DIR", materials_dir),
                patch.object(
                    generate_materials_overview,
                    "GENERATED_VIEWERS_DIR",
                    viewers_dir,
                ),
            ):
                content = generate_materials_overview.viewer_content(source_path)

        front_matter = content.split("---", 2)[1]
        metadata = generate_materials_overview.yaml.safe_load(front_matter)
        self.assertEqual(metadata["execute"], {"enabled": False})
        self.assertTrue(metadata["code-copy"])
        self.assertNotIn("execute: false", content)
        self.assertIn('```{.python filename="example.py"}', content)

    def test_no_generated_viewer_uses_scalar_execute_false(self):
        viewers = generate_materials_overview.GENERATED_VIEWERS_DIR.rglob("*.qmd")
        for viewer in viewers:
            with self.subTest(viewer=viewer):
                self.assertNotIn("execute: false", viewer.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
