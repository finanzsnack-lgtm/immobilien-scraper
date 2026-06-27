FROM python:3.11-slim

WORKDIR /app

# Installiere Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere Script
COPY scraper.py .

# Starte den Scraper
CMD ["python", "scraper.py"]
