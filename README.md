[README.md](https://github.com/user-attachments/files/29422529/README.md)
# 🏠 Immobilien-Scraper Hannover

Automatisches System zum Crawlen neuer Wohnungen in Hannover mit KI-gestützter Analyse und Email-Benachrichtigungen.

## 🎯 Features

- **Tägliches Crawling (3x täglich)** von Immoscout24 & Immowelt
- **Automatische Filterung** nach Preis (100k-200k€), Lage (Hannover + 20km Radius), Wohnungen
- **KI-Analyse mit Claude** - prüft:
  - Ist der Preis fair?
  - Ist die Lage gut für Vermietung?
  - Worauf bei der Besichtigung achten?
  - Wie sollte die Wohnung aussehen (Bad, Küche, etc.)?
- **Email-Benachrichtigungen** mit Listings + Analysen
- **Kostenlos** auf Render.com gehostet

## 🚀 Quick Start

### 1. API Keys besorgen

**Anthropic API Key** (für KI):
- Gehe zu: https://console.anthropic.com/
- Registriere dich kostenlos
- Erstelle einen neuen API Key

**Gmail App-Passwort** (für Email):
- Gehe zu: https://myaccount.google.com/apppasswords
- Wähle "Mail" + "Windows"
- Kopiere das 16-Zeichen Passwort

### 2. Auf Render.com deployen

1. Gehe zu: https://render.com
2. Registriere dich mit GitHub
3. Klick "New +" → "Cron Job"
4. Verbinde dieses Repository
5. Setze diese Umgebungsvariablen:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxx
   SENDER_EMAIL=deine-email@gmail.com
   SENDER_PASSWORD=app-passwort
   ```
6. Cron Schedule (3x täglich):
   ```
   0 7 * * *
   0 13 * * *
   0 19 * * *
   ```

✅ Fertig! Das System läuft jetzt automatisch.

## 📁 Projektstruktur

```
immobilien-scraper/
├── scraper.py              # Haupt-Crawler mit KI-Analyse
├── requirements.txt        # Python Dependencies
├── Dockerfile             # Docker Image
├── docker-compose.yml     # Lokal testen
├── .env.example           # Template für Umgebungsvariablen
├── .gitignore            # Git Ignore Rules
├── SETUP_ANLEITUNG.md    # Detaillierte Setup-Anleitung
└── README.md             # Diese Datei
```

## 🧪 Lokal testen

```bash
# 1. Repository klonen
git clone https://github.com/finanzsnack-lgtm/immobilien-scraper.git
cd immobilien-scraper

# 2. Dependencies installieren
pip install -r requirements.txt

# 3. .env erstellen und ausfüllen
cp .env.example .env
# Bearbeite .env mit deinen API Keys

# 4. Script ausführen
python scraper.py
```

## ⚙️ Konfiguration

In `scraper.py` anpassbar:

```python
MIN_PRICE = 100000      # Min. Kaufpreis
MAX_PRICE = 200000      # Max. Kaufpreis
LOCATION = "Hannover"   # Ort
RADIUS_KM = 20          # Umkreis in km
TARGET_EMAIL = "email@example.com"  # Ziel-Email
```

## 🐛 Troubleshooting

**"ANTHROPIC_API_KEY not set"**
→ Überprüfe Render.com Environment Variables

**"Gmail Login fehlgeschlagen"**
→ Nutze App-Passwort, nicht dein normales Passwort

**"Keine Emails angekommen"**
→ Schau im Spam-Ordner nach

**Scraper crasht auf Render**
→ Schau in Render Cron Job → Logs

## 📧 Email-Format

Emails enthalten:
- Titel & Preis der Wohnung
- Link zur Anzeige
- Quelle (Immoscout24 / Immowelt)
- Detaillierte KI-Analyse zur Vermietbarkeit

## 🔐 Sicherheit

- `.env` Datei ist in `.gitignore` (deine Secrets bleiben privat)
- API Keys werden nie ins Repository gepusht
- Alle sensiblen Daten als Render Environment Variables

## 📞 Support

Siehe `SETUP_ANLEITUNG.md` für detailliertere Hilfe.

## 📄 Lizenz

MIT

---

**Viel Erfolg bei der Wohnungssuche in Hannover! 🏠**
