# Google Maps Scraper

Ce projet permet de **scraper des fiches Google Maps**, et de stocker automatiquement les données dans une base SQLite.

> Fonctionne sous Windows uniquement

---

## Prérequis

### 1. Installer Python (3.10 ou plus)

- Télécharger depuis : https://www.python.org/downloads/
- **Pendant l’installation**, cocher `Add Python to PATH`

### 2. Installer Google Chrome (si ce n'est pas déjà fait évidemment)

- https://www.google.com/chrome/

### 4. Installer l’extension

- Se rendre à d'adresse suivante (modifier par votre nom d'utilisateur) : `C:\Users\<NOM_UTILISATEUR>\AppData\Local\Google\Chrome\User Data\Default\Extensions`

- Y glisser le dossier `mjllncbijgeccmolnikpkbkpbjggcgij`
- Dans le fichier `scraper.py`, modifier également le chemin d'accès à l'extension avec le vrai nom d'utilisateur

---

## Installation du projet

### 1. Cloner le dépôt

```bash
git clone https://github.com/DarioNonis/scraper.git
cd scraper
```

### 2. Installer les dépendances

```bash
python -m playwright install
```

### 3. Lancer le scraping

```bash
python scraper.py
```

> Un fichier `resultats.db` va alors être créé, pour visualiser son contenu il est possible de télécharger l'extension SQLite Viewer. Attention, toute modification de ce fichier pendant le scraping est susceptible de bloquer la base de données.

