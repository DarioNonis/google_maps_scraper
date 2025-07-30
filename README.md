# Google Maps Scraper

Ce projet permet de **scraper des fiches Google Maps** et de stocker automatiquement les données dans une base SQLite.

> Fonctionne uniquement sous **Windows** pour le moment.

---

## Prérequis

### 1. Installer Python (3.10 ou plus)

- Télécharger depuis : https://www.python.org/downloads/windows/
- Lors de l’installation :
  - **Cocher** l’option `Add Python to PATH`
  - Puis cliquer sur "Install Now"

> Si Python n’est pas reconnu dans le terminal après installation, consulter la section [Dépannage PATH](#dépannage-path)

---

### 2. Installer Google Chrome (si ce n'est pas déjà fait évidemment)

- Télécharger ici : https://www.google.com/chrome/

---

## Installation du projet

### 1. Cloner le dépôt

```bash
git clone https://github.com/DarioNonis/google_maps_scraper.git
cd google_maps_scraper
```

### 2. Installer Playwright et ses navigateurs

```bash
pip install playwright
python -m playwright install
```

> Si `pip` n'est pas reconnu, installez-le :  
> `python -m ensurepip --default-pip`

---

### 3. Installer l'extension Scrap.io

- Télécharger l’extension Scrap.io Chrome depuis le Chrome Web Store : [aller à la page](https://chromewebstore.google.com/detail/scrapio/mjllncbijgeccmolnikpkbkpbjggcgij)
- Trouver son chemin sur votre machine (faire attention à bien sélectionner le profil sur lequel l'extension est installée) :
  ```
  C:\Users\<NOM_UTILISATEUR>\AppData\Local\Google\Chrome\User Data\<PROFIL_CHROME>\Extensions\mjllncbijgeccmolnikpkbkpbjggcgij\<VERSION>
  ```
- Copier ce chemin, et **remplacer** la constante `EXTENSION_PATH` dans `scraper.py` par le chemin complet.

---

## Lancement

### 1. Initialiser la base de données

```bash
python db.py
```

### 2. Lancer le scraper

```bash
python scraper.py
```

> Les données seront automatiquement enregistrées dans un fichier `resultats.db`.  
> Vous pouvez l’ouvrir avec un outil comme [SQLite Viewer](https://sqlitebrowser.org/).

---

## Dépannage PATH

### Si `python` n’est pas reconnu ou ouvre le Microsoft Store

1. Ouvrir **"Gérer les alias d’exécution d'application"** dans le menu démarrer.
2. **Désactiver** les alias pour `python.exe` ou `python3.exe` par exemple.
3. Vérifier que le dossier réel de Python est bien dans le `PATH`. Exemple :
   ```
   C:\Users\<NOM_UTILISATEUR>\AppData\Local\Programs\Python\Python312\
   C:\Users\<NOM_UTILISATEUR>\AppData\Local\Programs\Python\Python312\Scripts\
   ```
   Ajouter un à un ces deux chemins dans : **Modifier les variables d'environnement système** > **Variables d'environnement** > `Path` > **Modifier** > **Nouveau**.