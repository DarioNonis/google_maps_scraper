import csv
import time
from playwright.sync_api import sync_playwright
from db import initialiser_db, inserer_fiches

FICHIER_RECHERCHES = "recherches.csv"

# Ajouter le chemin vers l'extension Scrap.io ci-dessous
EXTENSION_PATH = r""

def scraper_google_maps(secteur, ville):
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="userdata-scrap",
            headless=False,
            args=[
                f"--disable-extensions-except={EXTENSION_PATH}",
                f"--load-extension={EXTENSION_PATH}"
            ]
        )
        page = context.pages[0]
        query = f"{secteur} {ville}"
        url = f"https://www.google.com/maps/search/{query}"
        print(f"\nRecherche : {query}")
        page.goto(url)

        try:
            page.wait_for_selector("button:has-text('Tout accepter')", timeout=2000)
            page.click("button:has-text('Tout accepter')")
            print("Consentement accepté")
            time.sleep(0.5)
        except:
            print("Aucun consentement détecté")

        try:
            page.wait_for_selector("input#searchboxinput", timeout=10000)
            page.fill("input#searchboxinput", query)
            page.keyboard.press("Enter")
            print("Recherche lancée")
        except:
            print("Erreur lors de la recherche")
            context.close()
            return []

        try:
            page.wait_for_selector("div[role='feed']", timeout=10000)
            print("Résultats chargés")
        except:
            print("Conteneur non détecté")
            context.close()
            return []

        print("Scroll...")

        feed_selector = "div[role=feed]"
        previous_count = -1
        stagnant_iterations = 0
        max_stagnant = 5
        max_scrolls = 60

        for _ in range(max_scrolls):
            page.evaluate("document.querySelector('div[role=feed]').scrollBy(0, 1000)")
            time.sleep(0.7)
            current_cards = page.query_selector_all("div.scrapio-card")
            current_count = len(current_cards)

            if current_count == previous_count:
                stagnant_iterations += 1
                if stagnant_iterations >= max_stagnant:
                    break
            else:
                stagnant_iterations = 0
                previous_count = current_count

        print("Scroll terminé")

        items = page.query_selector_all("div.Nv2PK")
        scrap_cards = page.query_selector_all("div.scrapio-card")
        print(f"{len(items)} résultats trouvés / {len(scrap_cards)} cartes Scrap.io")

        results = []

        for i, item in enumerate(items):
            try:
                nom_elem = item.query_selector("a.hfpxzc")
                nom = nom_elem.get_attribute("aria-label").strip() if nom_elem else ""
                lien = nom_elem.get_attribute("href") if nom_elem else ""

                secteur_activite = ""
                adresse = ""
                try:
                    w4_blocks = item.query_selector_all("div.W4Efsd")
                    if w4_blocks:
                        last_block = w4_blocks[-2]
                        spans = last_block.query_selector_all("span")
                        if len(spans) >= 2:
                            secteur_activite = spans[0].inner_text().strip()
                            adresse = spans[-1].inner_text().strip().lstrip("· ")
                except:
                    pass

                note_elem = item.query_selector("span.MW4etd[aria-hidden='true']")
                avis_elem = item.query_selector("span.UY7F9[aria-hidden='true']")
                note = f"{note_elem.inner_text().strip()} {avis_elem.inner_text().strip()}" if note_elem and avis_elem else ""

                tel = site = email = facebook = instagram = linkedin = twitter = youtube = ""

                if i < len(scrap_cards):
                    scrap = scrap_cards[i]

                    def extract(selector):
                        el = scrap.query_selector(f"div[data-type='{selector}']")
                        return el.get_attribute("data-url") if el else ""

                    email = extract("emails").replace("mailto:", "")
                    facebook = extract("facebook")
                    instagram = extract("instagram")
                    linkedin = extract("linkedin")
                    twitter = extract("twitter")
                    youtube = extract("youtube")
                    tel = extract("phone_international").replace("tel:", "")
                    site = extract("website")

                results.append({
                    "Secteur": secteur_activite,
                    "Nom de l'entreprise": nom,
                    "Adresse postale": adresse,
                    "Numéro De Telephone": tel,
                    "Note": note,
                    "Site": site,
                    "Lien": lien,
                    "Email": email,
                    "Facebook": facebook,
                    "Instagram": instagram,
                    "LinkedIn": linkedin,
                    "Twitter": twitter,
                    "YouTube": youtube,
                    "Code postal et Ville": ""  # sera géré plus tard
                })

            except Exception as e:
                print(f"Erreur parsing élément : {e}")
                continue

        context.close()
        return results

def lire_recherches():
    with open(FICHIER_RECHERCHES, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        return [(ligne[0].strip(), ligne[1].strip()) for ligne in reader if len(ligne) == 2]

if __name__ == "__main__":
    initialiser_db()  # nouvelle initialisation SQLite
    toutes_les_recherches = lire_recherches()
    for secteur, ville in toutes_les_recherches:
        fiches = scraper_google_maps(secteur, ville)
        inserer_fiches(fiches)
