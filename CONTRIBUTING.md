# Beiträge zum Plan-Datenkatalog

1. Drittanbieter-Dateien niemals automatisiert spiegeln.
2. Vor jedem PDF-Commit muss je Datei eine dokumentierte Weiterveröffentlichungsfreigabe oder kompatible offene Lizenz vorliegen.
3. Die Rechtebasis wird im Manifest als prüfbarer Verweis hinterlegt. Keine Geheimnisse, Verträge oder privaten Nachweise in dieses öffentliche Repository committen.
4. `python3 tools/validate_catalog.py` und `python3 -m unittest tools/test_validate_catalog.py` ausführen.
5. Änderungen über einen Pull Request gegen `main` einreichen.

Der Katalog ist ein Freigabekanal, keine Sammlung bloßer Download-Links.
