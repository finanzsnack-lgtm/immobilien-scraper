#!/usr/bin/env python3
"""
Immobilien Web Scraper für Hannover
Crawlt Immoscout24 und Immowelt nach Wohnungen (100k-200k€)
Analysiert mit KI, ob Preis & Lage stimmen
Sendet Email-Benachrichtigungen mit Inspektions-Checkliste
"""

import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import anthropic
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.parse import quote, urlencode
import time

# ============ KONFIGURATION ============
TARGET_EMAIL = "nick.poeppler@outlook.de"
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "immobilien-bot@example.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")  # Wird via Env-Variable gesetzt
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

MIN_PRICE = 100000
MAX_PRICE = 200000
LOCATION = "Hannover"
RADIUS_KM = 20

# ============ IMMOSCOUT24 SCRAPER ============
def scrape_immoscout24():
    """Crawlt Immoscout24 nach Wohnungen"""
    listings = []

    try:
        # Immoscout24 Search URL
        url = f"https://www.immobilienscout24.de/Suche/S-T/Wohnung-Kauf/{LOCATION}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')

        # Suche nach Immobilien-Listen-Items
        # Hinweis: Selektoren können sich ändern, ggf. anpassen
        for item in soup.find_all('article', {'data-is-live-ad': 'true'}):
            try:
                # Titel & Link
                title_elem = item.find('h2', class_='font-semibold')
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                link_elem = item.find('a', href=True)
                link = link_elem['href'] if link_elem else ""

                # Preis
                price_elem = item.find('div', class_='text-2xl')
                price_text = price_elem.get_text(strip=True) if price_elem else "0"
                price = extract_price(price_text)

                # Größe & Zimmer
                details_text = item.get_text()

                # Filter nach Preis
                if MIN_PRICE <= price <= MAX_PRICE:
                    listings.append({
                        'title': title,
                        'price': price,
                        'link': link,
                        'source': 'Immoscout24',
                        'scraped_at': datetime.now().isoformat()
                    })

            except Exception as e:
                print(f"Fehler beim Parsen eines Immoscout24-Items: {e}")
                continue

        print(f"✓ Immoscout24: {len(listings)} Listings gefunden")

    except Exception as e:
        print(f"✗ Immoscout24 Scraping Fehler: {e}")

    return listings

# ============ IMMOWELT SCRAPER ============
def scrape_immowelt():
    """Crawlt Immowelt nach Wohnungen"""
    listings = []

    try:
        # Immowelt Search URL
        url = f"https://www.immowelt.de/immobilien/Wohnung-Kauf-{LOCATION}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')

        # Suche nach Immobilien-Listen-Items
        for item in soup.find_all('div', class_='result-item'):
            try:
                # Titel & Link
                title_elem = item.find('h2')
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                link_elem = item.find('a', href=True)
                link = link_elem['href'] if link_elem else ""

                # Preis
                price_elem = item.find('div', class_='price')
                price_text = price_elem.get_text(strip=True) if price_elem else "0"
                price = extract_price(price_text)

                # Filter nach Preis
                if MIN_PRICE <= price <= MAX_PRICE:
                    listings.append({
                        'title': title,
                        'price': price,
                        'link': link,
                        'source': 'Immowelt',
                        'scraped_at': datetime.now().isoformat()
                    })

            except Exception as e:
                print(f"Fehler beim Parsen eines Immowelt-Items: {e}")
                continue

        print(f"✓ Immowelt: {len(listings)} Listings gefunden")

    except Exception as e:
        print(f"✗ Immowelt Scraping Fehler: {e}")

    return listings

# ============ HILFS-FUNKTIONEN ============
def extract_price(price_text):
    """Extrahiert Preis aus Text (z.B. '150.000 €' -> 150000)"""
    import re
    numbers = re.findall(r'\d+', price_text.replace('.', '').replace(',', ''))
    return int(numbers[0]) if numbers else 0

def deduplicate_listings(listings):
    """Entfernt Duplikate basierend auf Titel"""
    seen = set()
    unique = []
    for listing in listings:
        if listing['title'] not in seen:
            seen.add(listing['title'])
            unique.append(listing)
    return unique

# ============ KI-ANALYSE (ANTHROPIC) ============
def analyze_with_ai(listing):
    """Analysiert mit Claude, ob Preis & Lage passen + Inspektions-Tipps"""

    if not ANTHROPIC_API_KEY:
        return {"error": "ANTHROPIC_API_KEY not set"}

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""
Du bist ein Immobilien-Experte für Vermietungen in Hannover.

Analysiere diese Wohnung:
- Titel: {listing['title']}
- Preis: {listing['price']}€
- Quelle: {listing['source']}
- Link: {listing['link']}

AUFGABEN:
1. Ist der Preis fair für Hannover? (100k-200k€ Range)
2. Ist die Lage (aus dem Titel erkennbar) gut für Vermietung?
3. Worauf sollte man bei der Besichtigung achten?
4. Wie sollte die Wohnung aussehen (Bad renoviert, Küche, etc.)?
5. Gesamtbewertung: Lohnt sich eine Besichtigung? (ja/nein mit Begründung)

Antworte strukturiert und prägnant.
"""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        analysis = message.content[0].text
        return {
            "status": "success",
            "analysis": analysis
        }

    except Exception as e:
        return {"error": f"KI-Analyse Fehler: {str(e)}"}

# ============ EMAIL-VERSAND ============
def send_email_notification(listings_with_analysis):
    """Sendet Email mit neuen Immobilien + KI-Analysen"""

    if not listings_with_analysis:
        print("Keine neuen Immobilien zum Versenden")
        return

    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("⚠ Email-Konfiguration fehlt (SENDER_EMAIL, SENDER_PASSWORD)")
        return

    # Email-Body zusammenstellen
    html_body = """
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>🏠 Neue Immobilien gefunden!</h2>
            <p>Crawl-Zeit: {}</p>
            <hr>
    """.format(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

    for listing in listings_with_analysis:
        html_body += f"""
        <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px;">
            <h3>{listing['title']}</h3>
            <p><strong>Preis:</strong> {listing['price']}€</p>
            <p><strong>Quelle:</strong> {listing['source']}</p>
            <p><a href="{listing['link']}" style="color: blue;">Zur Anzeige →</a></p>

            <h4>📊 KI-Analyse:</h4>
            <pre style="background-color: #f5f5f5; padding: 10px; border-radius: 3px;">
{listing.get('analysis', 'Analyse nicht verfügbar')}
            </pre>
        </div>
        """

    html_body += """
        </body>
    </html>
    """

    # Email versenden
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🏠 {len(listings_with_analysis)} neue Immobilie(n) in Hannover"
        msg['From'] = SENDER_EMAIL
        msg['To'] = TARGET_EMAIL

        msg.attach(MIMEText(html_body, 'html'))

        # Gmail SMTP (Falls du Gmail verwendest, sonst anpassen)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"✓ Email versendet an {TARGET_EMAIL}")

    except Exception as e:
        print(f"✗ Email-Versand Fehler: {e}")

# ============ HAUPT-FUNKTION ============
def main():
    print(f"\n{'='*50}")
    print(f"🔍 Immobilien-Scraper Start ({datetime.now().strftime('%H:%M:%S')})")
    print(f"{'='*50}")

    # Crawlen
    listings_immoscout = scrape_immoscout24()
    listings_immowelt = scrape_immowelt()

    all_listings = listings_immoscout + listings_immowelt
    unique_listings = deduplicate_listings(all_listings)

    print(f"\n📊 Gesamt: {len(unique_listings)} einzigartige Listings")

    # KI-Analysen durchführen
    print("\n🤖 Starte KI-Analysen...")
    listings_with_analysis = []

    for listing in unique_listings[:5]:  # Limit auf 5 pro Lauf (sparen Kosten)
        print(f"  → Analysiere: {listing['title'][:50]}...")
        analysis = analyze_with_ai(listing)

        listing['analysis'] = analysis.get('analysis', analysis.get('error', 'Fehler'))
        listings_with_analysis.append(listing)

        time.sleep(1)  # Rate-Limiting

    # Email versenden
    if listings_with_analysis:
        print("\n📧 Versende Email...")
        send_email_notification(listings_with_analysis)

    print(f"\n✓ Scraper beendet ({datetime.now().strftime('%H:%M:%S')})")

if __name__ == "__main__":
    main()
