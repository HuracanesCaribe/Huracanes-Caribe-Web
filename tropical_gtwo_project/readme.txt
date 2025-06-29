# Huracanes Caribe – Tropical Weather Outlook Map Generator

This Python project generates customized 2-day and 7-day tropical weather outlook maps for the Atlantic and Eastern Pacific basins, based on NOAA/NHC GTWO shapefiles.

---

## 🚀 Features
- Dynamic coloring for 2-day and 7-day outlooks
- Cairo-rendered vector arrows for system movement
- Localized issue times (Eastern or Pacific Time)
- Custom labels and legends
- High-resolution output PNGs

---

## 🛠 Requirements

Install dependencies using:
```bash
pip install -r requirements.txt
```

Make sure you’re using **Python 3.9+** (for built-in `zoneinfo`).

---

## 📂 Folder Structure
```
tropical_gtwo_project/
├── main.py              # Entry point
├── two_plot.py          # Core logic for one basin
├── two_data.py          # Downloads + reads shapefiles
├── two_map.py           # Drawing map + elements
├── config.py            # Settings + paths
├── requirements.txt     # Dependencies
├── output/              # Saved PNGs
└── data/                # Cached NOAA ZIPs
```

---

## 🧪 Usage

Run the generator:
```bash
python main.py
```
This will produce maps for both Atlantic and Eastern Pacific basins, saving them as:
```
output/atlantic_YYYYMMDDTHHMMZ.png
output/eastpac_YYYYMMDDTHHMMZ.png
```

---

## ⚙️ Optional: Run on a Schedule (cron)
To run this every 6 hours on a Linux system:
```cron
0 */6 * * * /usr/bin/python3 /path/to/tropical_gtwo_project/main.py
```

---

## 💬 Contact / Credits
Created by **Huracanes Caribe** – www.HuracanesCaribe.com  
Based on data from the [National Hurricane Center](https://www.nhc.noaa.gov/)
