# SEV Driver Assistant – Plan-Daten

Dieses **öffentliche Datenrepository** ist der kontrollierte Veröffentlichungsweg für SEV-Lagepläne, die ausdrücklich zur Weiterveröffentlichung freigegeben sind.

## Aktueller Stand

Der Katalog ist absichtlich leer. Die bisher von `bahnhof.de` referenzierten DB-PDFs werden hier **nicht** gespiegelt: DB InfraGO weist in den Nutzungsbedingungen darauf hin, dass jede andere Nutzung ihrer Webinhalte der vorherigen schriftlichen Zustimmung bedarf. Eine öffentliche Download-URL ist keine Spiegel- oder Verteilfreigabe.

## Aufnahme eines Plans

Ein PDF darf erst unter `pdf/` aufgenommen werden, wenn für genau diese Datei eine nachvollziehbare Rechtebasis vorliegt:

- schriftliche Weiterveröffentlichungsfreigabe des Rechteinhabers oder
- kompatible offene Lizenz.

Jeder Eintrag in `catalog/manifest.json` dokumentiert Datei, SHA-256, Bytegröße, Quelle und Rechtebasis. Die CI akzeptiert nur PDF-Dateien, die exakt zu einem Manifest-Eintrag passen und deren Integrität erfüllen.

Die Android-App verwendet später ausschließlich freigegebene Dateien aus einem versionierten GitHub-Release dieses Repositories. Sie enthält weder GitHub-Token noch Zugangsdaten. Bereits geprüfte Downloads bleiben lokal offline verfügbar.

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
