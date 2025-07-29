import sqlite3
import time

DB_PATH = "resultats.db"

def get_connection(retries=5, delay=1):
    for attempt in range(retries):
        try:
            conn = sqlite3.connect(DB_PATH, timeout=30)
            conn.execute("PRAGMA journal_mode=WAL;")
            return conn
        except sqlite3.OperationalError as e:
            print(f"Base verrouillée (tentative {attempt+1}/{retries}), attente...")
            time.sleep(delay)
    raise Exception("Échec connexion SQLite après plusieurs tentatives.")

def initialiser_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fiches (
                lien TEXT PRIMARY KEY,
                secteur TEXT,
                nom TEXT,
                adresse TEXT,
                telephone TEXT,
                note TEXT,
                site TEXT,
                email TEXT,
                facebook TEXT,
                instagram TEXT,
                linkedin TEXT,
                twitter TEXT,
                youtube TEXT,
                code_postal_ville TEXT
            )
        """)
        conn.commit()

def inserer_fiches(fiches):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            nouvelles = 0
            for f in fiches:
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO fiches VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        f["Lien"],
                        f["Secteur"],
                        f["Nom de l'entreprise"],
                        f["Adresse postale"],
                        f["Numéro De Telephone"],
                        f["Note"],
                        f["Site"],
                        f["Email"],
                        f["Facebook"],
                        f["Instagram"],
                        f["LinkedIn"],
                        f["Twitter"],
                        f["YouTube"],
                        f["Code postal et Ville"]
                    ))
                    nouvelles += cursor.rowcount
                except Exception as e:
                    print(f"Erreur insertion : {e}")
            conn.commit()
            print(f"{nouvelles} fiches insérées.")
    except Exception as e:
        print(f"Échec accès base : {e}")
