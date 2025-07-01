# Huracanes Caribe Web

This repository generates tropical weather outlook maps and provides a small viewer to browse the images.

## 1. Install dependencies

Ensure you have **Python 3.9+** and run:

```bash
pip install -r tropical_gtwo_project/requirements.txt
```

## 2. Generate the maps

Run the main script to download data and create the latest 2-day and 7-day GTWO plots for both basins:

```bash
python tropical_gtwo_project/main.py
```

The PNG files are saved under `tropical_gtwo_project/output/`.

## 3. Start the viewer

Launch the Flask server to expose the images and a JSON listing:

```bash
python web.py
```

Open `http://localhost:5000/` in your browser to see a basic gallery. The optional page `public/plots.html` uses the same server and displays the images in a grid.

## 4. Extra options

- Run `python tropical_gtwo_project/main.py --help` to see arguments for selecting a basin or custom output path.
- Automate the generator with cron if you need regular updates.
