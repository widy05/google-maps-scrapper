import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
from selenium.common.exceptions import TimeoutException

def get_email_from_site(driver, site_url):
    if not site_url:
        return ""
    try:
        driver.get("https://" + site_url if not site_url.startswith("http") else site_url)
        time.sleep(2)
        page = driver.page_source
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', page)
        # Filtrer les emails génériques/faux
        emails = [e for e in emails if not any(x in e for x in ['@sentry', '@example', '@google', '@schema', 'wix.com'])]
        return emails[0] if emails else ""
    except:
        return ""

def get_text(driver, xpath):
    try:
        return driver.find_element(By.XPATH, xpath).text.strip()
    except:
        return ""

def scrape_google_maps(keyword, ville, nb_resultats=20):
    query = f"{keyword} {ville}"
    url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"

    options = webdriver.ChromeOptions()
    options.add_argument("--lang=fr")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get(url)
    time.sleep(4)

    # Scroll pour charger les résultats
    wait = WebDriverWait(driver, 10)
    scrollable = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]')))
    for _ in range(5):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable)
        time.sleep(2)

    # Récupérer les liens
    listings = driver.find_elements(By.XPATH, '//a[@class="hfpxzc"]')
    links = [l.get_attribute("href") for l in listings[:nb_resultats]]
    print(f"🔍 {len(links)} fiches trouvées, démarrage du scraping...")

    results = []

    for link in links:
        driver.get(link)
        time.sleep(3)

        nom      = get_text(driver, '//h1')
        note     = get_text(driver, '//div[@jsaction]//span[@aria-hidden="true"][1]')
        adresse  = get_text(driver, '//button[@data-item-id="address"]//div[contains(@class,"fontBodyMedium")]')
        tel      = get_text(driver, '//button[contains(@data-item-id,"phone")]//div[contains(@class,"fontBodyMedium")]')
        site     = get_text(driver, '//a[@data-item-id="authority"]//div[contains(@class,"fontBodyMedium")]')
        email = get_email_from_site(driver, site)
        categorie = get_text(driver, '//button[@jsaction and contains(@class,"DkEaL")]')

        if nom:
            results.append({
                "Nom": nom,
                "Catégorie": categorie,
                "Note": note,
                "Adresse": adresse,
                "Téléphone": tel,
                "Site web": site,
                "Email": email,
                "URL Maps": link
            })
            print(f"✅ {nom} | {tel} | {note}")
        else:
            print("⚠️ Fiche ignorée (nom vide)")

    driver.quit()

    df = pd.DataFrame(results)
    filename = f"{keyword}_{ville}.csv".replace(" ", "_")
    df.to_csv(filename, index=False)
    print(f"\n✅ {len(results)} résultats sauvegardés dans {filename}")

# --- Lance ici ---
if __name__ == "__main__":
    keyword = input("🔍 Mot-clé (ex: restaurant, coiffeur, plombier) : ")
    ville = input("📍 Ville : ")
    nb = input("📊 Nombre de résultats (défaut 20) : ")
    nb = int(nb) if nb.strip().isdigit() else 20
    scrape_google_maps(keyword, ville, nb_resultats=nb)