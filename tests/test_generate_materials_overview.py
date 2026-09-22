from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import generate_materials_overview


class MaterialsOverviewTest(unittest.TestCase):
    def test_generated_content_includes_excel_cheat_sheet(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            materials_dir = Path(tmpdir)
            (materials_dir / "excel-cheat-sheet.pdf").touch()

            with patch.object(generate_materials_overview, "MATERIALS_DIR", materials_dir):
                content = generate_materials_overview.generated_content(
                    generate_materials_overview.publishable_files()
                )

        self.assertIn(
            "[Excel cheat sheet](materials/excel-cheat-sheet.pdf) | PDF",
            content,
        )


if __name__ == "__main__":
    unittest.main()
