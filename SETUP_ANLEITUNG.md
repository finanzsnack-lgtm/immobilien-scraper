# 🏠 Immobilien-Scraper Setup Anleitung

Ein automatisches System, das täglich neue Wohnungen in Hannover crawlt, mit KI analysiert und dir per Email benachrichtigt.

---

## 📋 Was das System tut

1. **Crawlt täglich 3x** (z.B. 07:00, 13:00, 19:00) Immoscout24 + Immowelt
2. **Filtert** nach Hannover (20km Radius), 100k-200k€, Wohnungen
3. **Analysiert mit KI**, ob:
   - Der Preis fair ist
   - Die Lage gut für Vermietung ist
   - Worauf man bei Besichtigung achten sollte
   - Wie die Wohnung aussehen sollte (Bad, Küche, etc.)
4. **Sendet Email** mit Listings + KI-Analyse

---

## 🔧 Schritt-für-Schritt Setup

### **Schritt 1: API-Keys besorgen**

#### A) Anthropic API Key (für KI-Analysen)
1. Gehe zu: https://console.anthropic.com/
2. Registriere dich (kostenlos)
3. Gehe zu "API Keys" → "Create new key"
4. Kopiere den Key (sieht so aus: `sk-ant-...`)
5. **Speichere diesen Key ab!**

#### B) Gmail App-Passwort (für Email-Versand)
1. Öffne: https://myaccount.google.com/
2. Links: "Sicherheit"
3. Scrolle zu "App-Passwörter" (nur sichtbar, wenn 2FA aktiviert ist!)
4. Wähle "Mail" + "Windows Computer"
5. Google gibt dir ein 16-Zeichen Passwort
6. **Speichere dieses Passwort ab!**

> **Problem:** Dein Account hat kein 2FA? Dann musst du es zuerst aktivieren: https://support.google.com/accounts/answer/185839

---

### **Schritt 2: GitHub Repository erstellen**

1. Gehe zu https://github.com/new
2. Repository-Name: `immobilien-scraper`
3. "Public" auswählen
4. "Create repository" klicken

5. Lade die Dateien hoch:
   - `scraper.py`
   - `requirements.txt`
   - `Dockerfile`
   - `.env.example`

**Oder via Git:**
```bash
git clone https://github.com/DEIN-USERNAME/immobilien-scraper.git
cd immobilien-scraper
git add .
git commit -m "Initial commit"
git push
```

---

### **Schritt 3: Auf Render.com deployen**

1. Gehe zu https://render.com
2. Registriere dich (mit GitHub)
3. Klicke auf "New +" → "Cron Job"
4. Verbinde dein GitHub Repository
5. Fülle aus:
   - **Name:** `immobilien-scraper`
   - **Repository:** Wähle dein GitHub Repo
   - **Branch:** `main`
   - **Runtime:** `Docker`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python scraper.py`

6. **Umgebungsvariablen setzen** (Environment):
   ```
   ANTHROPIC_API_KEY=sk-ant-xxx (Dein API Key)
   SENDER_EMAIL=deine-email@gmail.com
   SENDER_PASSWORD=dein-app-passwort
   ```

7. **Cron Schedule setzen:**
   ```
   0 7 * * *  (täglich 07:00 Uhr)
   0 13 * * * (täglich 13:00 Uhr)
   0 19 * * * (täglich 19:00 Uhr)
   ```

8. Klicke "Create Cron Job"

✅ **Fertig!** Das System läuft jetzt automatisch 3x täglich.

---

## 🧪 Lokal testen

Falls du das System vor dem Upload testen möchtest:

```bash
# 1. Dependencies installieren
pip install -r requirements.txt

# 2. .env Datei erstellen
cp .env.example .env
# Editiere .env und füge deine API Keys ein

# 3. Script ausführen
python scraper.py
```

---

## 📧 Emails anpassen

Die Emails werden in HTML formatiert versendet. Um das Layout zu ändern, editiere diese Funktion in `scraper.py`:

```python
def send_email_notification(listings_with_analysis):
    # ... hier kannst du den HTML anpassen ...
```

---

## 🐛 Troubleshooting

### "ANTHROPIC_API_KEY not set"
→ Du hast den API Key nicht in Render.com eingestellt. Gehe zu Cron Job Settings → Environment.

### "Gmail Login fehlgeschlagen"
→ Kontrolliere, dass du:
- Ein **App-Passwort** verwendest (nicht dein normales Passwort)
- 2FA in deinem Google Account aktiviert ist

### "Keine Emails angekommen"
→ Schau in deinen Spam-Ordner! Gmail könnte die Emails dort landen.

### "Scraper crasht auf Render"
→ Gehe zu Cron Job → "Logs" und schau nach Fehler-Meldungen.

---

## 💡 Tipps & Tweaks

### Anzahl Listings pro Email begrenzen
In `scraper.py`, Zeile ~220:
```python
for listing in unique_listings[:5]:  # Max. 5 pro Lauf
```
Ändern auf deine Wunschzahl.

### Nur bestimmte Stadtteile
In `scraper.py`, die `LOCATION` Variable anpassen:
```python
LOCATION = "Hannover-Süd"  # Statt nur "Hannover"
```

### Cron-Zeiten anpassen
In Render → Cron Job Settings:
```
0 6 * * *   → 06:00 Uhr
0 12 * * *  → 12:00 Uhr
0 18 * * *  → 18:00 Uhr
```

---

## 📞 Support

Falls es Probleme gibt:
1. Schau in Render.com → Logs
2. Teste lokal mit `python scraper.py`
3. Überprüfe deine API Keys

---

**Viel Erfolg bei der Wohnungssuche! 🏠**
