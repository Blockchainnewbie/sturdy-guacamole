
-----

### Schritt-für-Schritt: Dein Python-Paket manuell auf PyPI hochladen

**Voraussetzungen:**

1.  **Python & pip:** Stelle sicher, dass Python und pip auf deinem System installiert und aktuell sind.
2.  **PyPI Account:** Du benötigst einen Account auf [PyPI](https://pypi.org/) und idealerweise auch auf [TestPyPI](https://test.pypi.org/) zum Testen.

-----

**Schritt 1: Projektstruktur erstellen**

Eine gute Struktur ist die halbe Miete\! 😉 Hier ist ein gängiges Layout:

```
mein_projekt_verzeichnis/
│
├── src/                     # Hier kommt dein eigentlicher Code rein
│   └── mein_paket_name/     # Der Name deines importierbaren Pakets
│       ├── __init__.py      # Macht das Verzeichnis zu einem Python-Paket
│       └── modul.py         # Dein(e) Python-Modul(e)
│
├── tests/                   # (Optional, aber empfohlen) Deine Unit-Tests
│   └── test_modul.py
│
├── pyproject.toml           # Die wichtigste Datei: Konfiguration & Metadaten
├── README.md                # Beschreibung deines Projekts (wird auf PyPI angezeigt)
├── LICENSE                  # Lizenzdatei (z.B. MIT, Apache 2.0)
└── .gitignore               # (Optional) Git-Konfiguration zum Ignorieren von Dateien
```

  * Ersetze `mein_projekt_verzeichnis` und `mein_paket_name` durch deine Wunschnamen.
  * Die `src/` Struktur ist modern und vermeidet einige häufige Import-Probleme.

-----

**Schritt 2: `pyproject.toml` erstellen und konfigurieren**

Diese Datei ist das Herzstück deines Pakets. Sie definiert, wie dein Paket gebaut wird und enthält alle Metadaten, die auf PyPI angezeigt werden.

Erstelle die Datei `pyproject.toml` im Hauptverzeichnis (`mein_projekt_verzeichnis/`) mit folgendem Inhalt (passe ihn entsprechend an):

```toml
# pyproject.toml

# Definiert das Build-System (wie dein Paket gebaut wird)
# Wir verwenden hier setuptools, den Quasi-Standard.
[build-system]
requires = ["setuptools>=61.0"]  # Mindestversion von setuptools
build-backend = "setuptools.build_meta" # Gibt an, wie setuptools die Builds durchführt

# Projekt-Metadaten (was auf PyPI angezeigt wird)
[project]
name = "mein-einzigartiges-paket" # Der Name, unter dem dein Paket auf PyPI gefunden wird (muss einzigartig sein!)
version = "0.1.0" # Die Version deines Pakets (folge SemVer: MAJOR.MINOR.PATCH)
authors = [
  # Liste der Autoren
  { name="Dein Name", email="deine@email.com" },
]
description = "Eine kurze, knackige Beschreibung meines Pakets." # Kurzbeschreibung
readme = "README.md" # Verweis auf die README-Datei für die lange Beschreibung
requires-python = ">=3.8" # Mindest-Python-Version, die benötigt wird
license = { file="LICENSE" } # Verweis auf die Lizenzdatei
keywords = ["python", "beispiel", "paket"] # Schlüsselwörter zur Suche auf PyPI
classifiers = [
    # PyPI-Klassifikatoren (siehe https://pypi.org/classifiers/)
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License", # Wähle deine Lizenz
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Operating System :: OS Independent", # Wenn dein Paket plattformunabhängig ist
]
dependencies = [
    # Liste hier externe Pakete auf, von denen dein Code abhängt
    # Beispiel: "requests>=2.20.0",
    #           "numpy",
]

# (Optional) URLs für dein Projekt
[project.urls]
Homepage = "https://github.com/dein-benutzer/dein-projekt" # Oder deine Website
"Bug Tracker" = "https://github.com/dein-benutzer/dein-projekt/issues"
```

  * **WICHTIG:** Wähle einen **einzigartigen `name`** für PyPI. Prüfe auf [pypi.org](https://pypi.org/), ob der Name schon vergeben ist.
  * Fülle die Metadaten sorgfältig aus. Eine gute `README.md` und passende `classifiers` sind Gold wert\! ✨
  * Denk an die `LICENSE`-Datei. Ohne Lizenz ist dein Code standardmäßig nicht Open Source. Wähle eine passende Lizenz (z.B. MIT, Apache 2.0) und lege den Lizenztext in die `LICENSE`-Datei.

-----

**Schritt 3: Build-Werkzeuge installieren**

Du brauchst zwei kleine Helferlein, um dein Paket zu bauen und hochzuladen: `build` und `twine`.

```bash
# Öffne dein Terminal im Projekt-Hauptverzeichnis (mein_projekt_verzeichnis/)
python -m pip install --upgrade build twine
```

  * `build`: Baut dein Paket in die standardisierten Formate (sdist und wheel).
  * `twine`: Lädt dein gebautes Paket sicher auf PyPI hoch.

-----

**Schritt 4: Dein Paket bauen**

Jetzt wird's ernst\! Erstellen wir die Distributionsdateien.

```bash
# Stelle sicher, dass du im Projekt-Hauptverzeichnis bist
python -m build
```

Dieser Befehl liest deine `pyproject.toml`, führt den Build-Prozess aus und erstellt einen neuen Ordner namens `dist/`. Darin findest du zwei Dateien:

1.  `mein_einzigartiges_paket-0.1.0.tar.gz`: Eine *Source Distribution* (sdist). Enthält deinen Quellcode und die Metadaten. Wird benötigt, wenn keine passende Wheel-Datei verfügbar ist oder zum Bauen auf anderen Systemen.
2.  `mein_einzigartiges_paket-0.1.0-py3-none-any.whl`: Eine *Built Distribution* (wheel). Dies ist das bevorzugte Format, da es schneller installiert werden kann (es ist quasi eine Zip-Datei mit kompilierten Teilen, falls nötig). `py3-none-any` bedeutet, dass es für Python 3 auf jeder Plattform ohne C-Extensions funktioniert.

Wenn alles geklappt hat, siehst du eine Erfolgsmeldung und den `dist/` Ordner. 😊

-----

**Schritt 5: Paket auf TestPyPI hochladen (Empfohlen\!)**

Bevor du dein Paket auf das "echte" PyPI loslässt, solltest du es auf TestPyPI ausprobieren. Das ist eine separate Instanz zum Testen.

```bash
# Lade die Dateien aus dem dist/-Ordner auf TestPyPI hoch
python -m twine upload --repository testpypi dist/*
```

  * `twine` wird dich nach deinem Benutzernamen und Passwort für **TestPyPI** fragen.
  * **Sicherheitstipp:** Verwende statt deines Passworts lieber einen **API Token**.
    1.  Gehe zu deinen Account-Einstellungen auf [TestPyPI](https://www.google.com/search?q=https://test.pypi.org/manage/account/%23api-tokens).
    2.  Erstelle einen neuen Token (du kannst den Scope auf ein bestimmtes Projekt beschränken).
    3.  **Kopiere den Token sofort\!** Er wird nur einmal angezeigt.
    4.  Wenn `twine` nach dem Benutzernamen fragt, gib `__token__` ein.
    5.  Wenn `twine` nach dem Passwort fragt, füge den kopierten API-Token ein.

Nach dem Upload kannst du auf `https://test.pypi.org/project/mein-einzigartiges-paket/` nachsehen, ob alles korrekt angezeigt wird. Du kannst es auch testweise installieren:

```bash
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps mein-einzigartiges-paket
```

-----

**Schritt 6: Paket auf das "echte" PyPI hochladen**

Wenn auf TestPyPI alles gut aussah, bist du bereit für den finalen Schritt\!

```bash
# Lade die Dateien aus dem dist/-Ordner auf das echte PyPI hoch
python -m twine upload dist/*
```

  * Diesmal fragt `twine` nach deinem Benutzernamen und Passwort für das **Haupt-PyPI** (`pypi.org`).
  * Auch hier gilt: **Benutze unbedingt einen API Token\!** Erstelle ihn genauso wie für TestPyPI, nur eben auf der [echten PyPI-Seite](https://www.google.com/search?q=https://pypi.org/manage/account/%23api-tokens). Gib wieder `__token__` als Benutzername und den Token als Passwort ein.

**Herzlichen Glückwunsch\!** 🎉 Dein Paket sollte nun auf `https://pypi.org/project/mein-einzigartiges-paket/` verfügbar sein und kann von jedem mit `pip install mein-einzigartiges-paket` installiert werden.

-----

**Zusammenfassung der Befehle:**

1.  `python -m pip install --upgrade build twine` (Einmalig installieren)
2.  `python -m build` (Paket bauen, erzeugt `dist/`)
3.  `python -m twine upload --repository testpypi dist/*` (Upload zu TestPyPI, mit `__token__` und API-Token)
4.  `python -m twine upload dist/*` (Upload zu PyPI, mit `__token__` und API-Token)

-----

Denk dran: Jedes Mal, wenn du eine neue Version deines Pakets veröffentlichen willst, musst du nur:

1.  Die `version` in `pyproject.toml` erhöhen (z.B. auf `0.1.1` oder `0.2.0`).
2.  Die Schritte 4, (optional 5) und 6 wiederholen.

Ich hoffe, diese Anleitung hilft dir weiter\! Wenn du auf Probleme stößt oder Fragen hast, frag einfach. Viel Erfolg beim Veröffentlichen deines Pakets\! 😊