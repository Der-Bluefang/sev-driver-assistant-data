# SEV Driver Assistant – Plan-Daten

Dieses **öffentliche Datenrepository** ist der kontrollierte Veröffentlichungsweg für SEV-Lagepläne, deren Weiterveröffentlichung für den SEV Driver Assistant ausdrücklich freigegeben wurde.

## Aktueller Stand

Der Katalog enthält **241 freigegebene SEV-PDFs** in Katalogversion **`1.1.0`**. Die jeweilige Rechtebasis ist als `written_permission` im Manifest dokumentiert. Der vollständige schriftliche Nachweis bleibt beim Projektinhaber und wird nicht in dieses öffentliche Repository übernommen.

Die Dateien stammen aus den im Manifest angegebenen Originalquellen. Beim Import wurden die aktuelle Datei, Größe, `%PDF-`-Signatur und SHA-256 geprüft. Die 194 in Version `1.1.0` ergänzten NRW-Pläne wurden zusätzlich gegen den im aktuellen PDF extrahierten Stationsnamen, einen eindeutigen RIL100-Code sowie ein dokumentiertes NRW-Bahnhofsmanagement geprüft. Ein Plan mit abweichender aktueller Identität wurde bewusst nicht aufgenommen.

## Aufnahme eines Plans

Ein PDF darf erst unter `pdf/` aufgenommen werden, wenn für genau diese Datei eine nachvollziehbare Rechtebasis vorliegt:

- schriftliche Weiterveröffentlichungsfreigabe des Rechteinhabers oder
- kompatible offene Lizenz.

Jeder Eintrag in `catalog/manifest.json` dokumentiert Datei, SHA-256, Bytegröße, Quelle und Rechtebasis. Die CI akzeptiert nur PDF-Dateien, die exakt zu einem Manifest-Eintrag passen und deren Integrität erfüllen.

Die Android-App verwendet ausschließlich freigegebene Dateien aus diesem versionierten Repository. Sie enthält weder GitHub-Token noch Zugangsdaten. Bereits geprüfte Downloads bleiben lokal offline verfügbar.

## Struktur

- `catalog/manifest.json` – maschinenlesbarer freigegebener Datenbestand
- `catalog/manifest.schema.json` – JSON-Schema des Datenbestands
- `pdf/` – ausschließlich freigegebene PDF-Dateien
- `tools/validate_catalog.py` – lokale und CI-Validierung

## Nutzung

```bash
python3 tools/validate_catalog.py
python3 -m unittest tools/test_validate_catalog.py
```
