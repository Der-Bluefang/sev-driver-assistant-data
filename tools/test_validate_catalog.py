from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_catalog import validate


class ValidateCatalogTest(unittest.TestCase):
    def create_root(self) -> Path:
        root = Path(tempfile.mkdtemp())
        (root / "catalog").mkdir()
        (root / "pdf").mkdir()
        return root

    def write_manifest(self, root: Path, plans: list[dict]) -> None:
        (root / "catalog" / "manifest.json").write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "catalogVersion": "1.0.0",
                    "generatedAt": "2026-07-20T00:00:00Z",
                    "plans": plans,
                },
            ),
            encoding="utf-8",
        )

    def test_accepts_empty_approved_catalog(self) -> None:
        root = self.create_root()
        self.write_manifest(root, [])
        self.assertEqual({"catalogVersion": "1.0.0", "plans": 0, "status": "valid"}, validate(root))

    def test_rejects_unlisted_pdf(self) -> None:
        root = self.create_root()
        self.write_manifest(root, [])
        (root / "pdf" / "unlisted.pdf").write_bytes(b"%PDF-test")
        with self.assertRaisesRegex(ValueError, "exactly one"):
            validate(root)

    def test_validates_pdf_checksum_rights_and_size(self) -> None:
        root = self.create_root()
        content = b"%PDF-approved"
        pdf = root / "pdf" / "essen-hbf.pdf"
        pdf.write_bytes(content)
        self.write_manifest(
            root,
            [
                {
                    "stationCode": "EE",
                    "stationName": "Essen Hbf",
                    "file": "pdf/essen-hbf.pdf",
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "bytes": len(content),
                    "sourceUrl": "https://example.org/approved/essen-hbf.pdf",
                    "rightsBasis": "open_license",
                    "rightsReference": "https://example.org/license",
                    "rightsVerifiedAt": "2026-07-20T00:00:00Z",
                },
            ],
        )
        self.assertEqual(1, validate(root)["plans"])

    def test_rejects_missing_rights_reference(self) -> None:
        root = self.create_root()
        content = b"%PDF-approved"
        (root / "pdf" / "essen-hbf.pdf").write_bytes(content)
        self.write_manifest(
            root,
            [
                {
                    "stationCode": "EE",
                    "stationName": "Essen Hbf",
                    "file": "pdf/essen-hbf.pdf",
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "bytes": len(content),
                    "sourceUrl": "https://example.org/approved/essen-hbf.pdf",
                    "rightsBasis": "written_permission",
                    "rightsReference": "",
                    "rightsVerifiedAt": "2026-07-20T00:00:00Z",
                },
            ],
        )
        with self.assertRaisesRegex(ValueError, "rightsReference"):
            validate(root)


if __name__ == "__main__":
    unittest.main()
