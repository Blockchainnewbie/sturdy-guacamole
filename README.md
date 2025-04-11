
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


# Von GitHub zu PyPI: Eine Schritt-für-Schritt Anleitung

Diese Anleitung erklärt, wie du ein Python-Paket von GitHub direkt zu PyPI hochladen kannst, mit einem automatischen Workflow über GitHub Actions und dem "Trusted Publisher"-System.

## Voraussetzungen

- Ein GitHub-Account
- Ein PyPI-Account
- Ein Python-Projekt mit einer gültigen `setup.py` oder `pyproject.toml`
- Git auf deinem lokalen Computer

## 1. PyPI Trusted Publisher einrichten

PyPI's "Trusted Publisher"-System ermöglicht es, Code direkt von GitHub zu veröffentlichen, ohne API-Tokens im Workflow speichern zu müssen.

### 1.1 PyPI-Konto vorbereiten

1. Logge dich bei [PyPI](https://pypi.org) ein
2. Gehe zu deinen **Konto-Einstellungen** → **Publishing**
3. Klicke auf "Add Publisher"
4. Fülle das Formular mit folgenden Werten aus:
   - Publisher: `GitHub Actions`
   - Owner: `dein-github-username` 
   - Repository: `dein-repo-name`
   - Workflow name: `Publish Python Package` (oder wie dein Workflow heißen wird)
   - Environment (optional): leer lassen oder spezifizieren, falls du es nutzt
5. Speichere die Einstellungen

## 2. GitHub Actions Workflow einrichten

Erstelle in deinem Repository eine Datei unter `.github/workflows/publish.yml` mit folgendem Inhalt:

```yaml
name: Publish Python Package

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # Wichtig für OIDC!
      
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish package
      uses: pypa/gh-action-pypi-publish@release/v1
      # Keine Token-Angabe mehr nötig, da wir Trusted Publisher verwenden
```

## 3. Erstes Paket manuell hochladen (nur einmalig notwendig)

**Wichtig**: Trusted Publishers können nur zu bereits existierenden Projekten veröffentlichen. Daher musst du dein Paket zunächst einmal manuell hochladen:

```bash
# Build-Pakete erstellen
python -m build

# Manuell zu PyPI hochladen
python -m twine upload dist/*
```

Bei der Ausführung von `twine upload` wirst du nach deinen PyPI-Zugangsdaten gefragt.

## 4. setup.py korrekt konfigurieren

Stelle sicher, dass deine `setup.py` korrekt konfiguriert ist. Hier ein Beispiel für eine gute `setup.py`:

```python
from setuptools import setup, find_packages

# README.md als long_description verwenden
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dein-paket-name",  # Muss exakt mit dem PyPI-Namen übereinstimmen!
    version="0.1.0",
    author="Dein Name",
    author_email="deine.email@example.com",
    description="Kurze Beschreibung des Pakets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/repository",
    project_urls={
        "Bug Tracker": "https://github.com/username/repository/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        # Abhängigkeiten hier auflisten
        "requests>=2.25.1",
    ],
)
```

⚠️ **Der Name in der setup.py muss exakt mit dem auf PyPI registrierten Namen übereinstimmen!**

## 5. Code ändern und veröffentlichen

Jedes Mal, wenn du eine neue Version veröffentlichen möchtest:

### 5.1 Version aktualisieren

Ändere die Versionsnummer in deiner `setup.py` oder `pyproject.toml`.

### 5.2 Änderungen zu GitHub übertragen

```bash
# Status überprüfen
git status

# Änderungen hinzufügen
git add .

# Commit erstellen
git commit -m "Version auf 0.1.1 aktualisiert"

# Zu GitHub pushen
git push origin main
```

### 5.3 Release auf GitHub erstellen

1. Gehe zu deinem Repository auf GitHub
2. Klicke auf "Releases" in der rechten Seitenleiste
3. Klicke auf "Draft a new release" oder "Create a new release"
4. Gib einen Tag-Namen ein (z.B. v0.1.1) - dieser sollte mit deiner package-Version übereinstimmen
5. Gib einen Titel für den Release ein
6. Füge Beschreibungen/Release Notes hinzu
7. Klicke auf "Publish release"

### 5.4 Workflow überprüfen

Nachdem du den Release erstellt hast:

1. Gehe zum "Actions" Tab in deinem GitHub Repository
2. Du solltest deinen Workflow "Publish Python Package" sehen, der ausgeführt wird
3. Warte, bis der Workflow abgeschlossen ist

Wenn alles richtig konfiguriert ist, wird dein Paket automatisch zu PyPI hochgeladen!

## Häufige Fehler und Lösungen

### "Non-user identities cannot create new projects"

Das bedeutet, dass entweder:
- Das Paket existiert noch nicht auf PyPI (löse durch manuelles erstmaliges Hochladen)
- Der Name in deiner setup.py stimmt nicht mit dem auf PyPI überein (passe den Namen an)

### "Filename or contents already exists"

Die Version, die du hochladen möchtest, existiert bereits auf PyPI. Du musst die Versionsnummer erhöhen.

### "Invalid or non-existent project name"

Der angegebene Name in deiner Konfiguration stimmt nicht mit einem auf PyPI existierenden Projekt überein.

## Tipps für gute Pakete

- **Dokumentation**: Erstelle eine gute README.md mit Installationsanweisungen und Beispielen
- **Tests**: Füge Tests hinzu, um die Qualität deines Codes sicherzustellen
- **Semantic Versioning**: Nutze [Semantic Versioning](https://semver.org/) für deine Versionsnummern
- **Changelog**: Führe eine CHANGELOG.md, um Änderungen zwischen Versionen zu dokumentieren

## Nützliche Ressourcen

- [PyPI Trusted Publishers Dokumentation](https://docs.pypi.org/trusted-publishers/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [GitHub Actions Dokumentation](https://docs.github.com/en/actions)