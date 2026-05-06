# 🗺️ Google Maps Lead Scraper

Automated tool to extract business leads from Google Maps and export them to CSV.

## 📦 What you get
| Field | Description |
|-------|-------------|
| Name | Business name |
| Category | Type of business |
| Rating | Google rating |
| Address | Full address |
| Phone | Phone number |
| Website | Website URL |
| Email | Contact email |
| Maps URL | Direct Google Maps link |

## ▶️ How to use
```bash
pip install selenium webdriver-manager pandas
python main.py
```
Enter keyword and city when prompted. CSV file is generated automatically.

## 💡 Examples
| Keyword | City | Output file |
|---------|------|-------------|
| restaurant | Paris | restaurant_Paris.csv |
| dentiste | Nice | dentiste_Nice.csv |
| coiffeur | Lyon | coiffeur_Lyon.csv |

## 🛠️ Tech stack
- Python 3.9
- Selenium + ChromeDriver
- Pandas

## 📬 Need custom leads?
Contact me on Upwork for a custom scraping service.
