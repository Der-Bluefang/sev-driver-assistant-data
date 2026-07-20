#!/usr/bin/env python3
"""Validate the approved SEV plan catalog without downloading external content."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

MAXIMUM_PDF_BYTES = 5 * 1024 * 1024
MANIFEST_FIELDS = {"schemaVersion", "catalogVersion", "generatedAt", "plans"}
PLAN_FIELDS = {
    "stationCode",
    "stationName",
    "file",
    "sha256",
    "bytes",
    "sourceUrl",
    "rightsBasis",
    "rightsReference",
    "rightsVerifiedAt",
}
STATION_CODE = re.compile(r"[A-Z0-9]{1,12}\Z")
SHA256 = re.compile(r"[a-f0-9]{64}\Z")
SEMVER = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+\Z")
SAFE_PDF = re.compile(r"pdf/[A-Za-z0-9][A-Za-z0-9._-]*\.pdf\Z")


def parse_timestamp(value: object, field: str) -> None:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"{field} is not an ISO-8601 timestamp") from error
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include a timezone")


def require_https_url(value: object, field: str) -> None:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a URL")
    url = urlsplit(value)
    if url.scheme != "https" or not url.hostname or url.username or url.password or url.fragment:
        raise ValueError(f"{field} must be a plain HTTPS URL")


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(64 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def validate(root: Path) -> dict[str, object]:
    root = root.resolve()
    manifest_path = root / "catalog" / "manifest.json"
    pdf_root = (root / "pdf").resolve()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != MANIFEST_FIELDS:
        raise ValueError("Manifest fields are incomplete or unexpected")
    if data["schemaVersion"] != 1:
        raise ValueError("Unsupported manifest schema")
    if not isinstance(data["catalogVersion"], str) or not SEMVER.fullmatch(data["catalogVersion"]):
        raise ValueError("Catalog version must be semantic versioning")
    parse_timestamp(data["generatedAt"], "generatedAt")
    if not isinstance(data["plans"], list):
        raise ValueError("plans must be an array")

    listed_files: set[Path] = set()
    station_codes: set[str] = set()
    for plan in data["plans"]:
        if not isinstance(plan, dict) or set(plan) != PLAN_FIELDS:
            raise ValueError("Plan fields are incomplete or unexpected")
        code = plan["stationCode"]
        relative = plan["file"]
        if not isinstance(code, str) or not STATION_CODE.fullmatch(code) or code in station_codes:
            raise ValueError("Station code is invalid or duplicated")
        if not isinstance(plan["stationName"], str) or not plan["stationName"].strip():
            raise ValueError("Station name is missing")
        if not isinstance(relative, str) or not SAFE_PDF.fullmatch(relative):
            raise ValueError("PDF path is unsafe")
        if not isinstance(plan["sha256"], str) or not SHA256.fullmatch(plan["sha256"]):
            raise ValueError("PDF checksum is invalid")
        if not isinstance(plan["bytes"], int) or isinstance(plan["bytes"], bool) or not 5 <= plan["bytes"] <= MAXIMUM_PDF_BYTES:
            raise ValueError("PDF size metadata is invalid")
        require_https_url(plan["sourceUrl"], "sourceUrl")
        if plan["rightsBasis"] not in {"written_permission", "open_license"}:
            raise ValueError("A documented redistribution rights basis is required")
        if not isinstance(plan["rightsReference"], str) or not plan["rightsReference"].strip():
            raise ValueError("rightsReference is required")
        parse_timestamp(plan["rightsVerifiedAt"], "rightsVerifiedAt")

        file_path = (root / relative).resolve()
        if file_path.parent != pdf_root or not file_path.is_file():
            raise ValueError("Referenced PDF is missing or outside the PDF directory")
        if file_path.stat().st_size != plan["bytes"] or file_path.stat().st_size > MAXIMUM_PDF_BYTES:
            raise ValueError("PDF byte length does not match the manifest")
        with file_path.open("rb") as stream:
            if stream.read(5) != b"%PDF-":
                raise ValueError("PDF signature is invalid")
        if digest(file_path) != plan["sha256"]:
            raise ValueError("PDF checksum does not match the manifest")
        listed_files.add(file_path)
        station_codes.add(code)

    actual_files = {path.resolve() for path in pdf_root.glob("*.pdf") if path.is_file()}
    if actual_files != listed_files:
        raise ValueError("Every PDF must have exactly one validated manifest record")
    return {"catalogVersion": data["catalogVersion"], "plans": len(data["plans"]), "status": "valid"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(validate(args.root), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Catalog validation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
