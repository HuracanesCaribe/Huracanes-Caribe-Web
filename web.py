import pathlib
from flask import Flask, send_from_directory, render_template_string, jsonify

app = Flask(__name__)
OUTDIR = pathlib.Path(__file__).resolve().parent / 'tropical_gtwo_project' / 'output'

@app.route('/')
def index():
    images = sorted(OUTDIR.glob('*.png'))
    items = '\n'.join(f'<li><img src="/plots/{img.name}" alt="{img.name}"></li>' for img in images)
    html = f"""
    <html><head><title>GTWO Plots</title>
    <style>body{{font-family:sans-serif;padding:20px}}img{{max-width:100%;height:auto;margin-bottom:20px}}</style>
    </head><body><h1>GTWO Plots</h1><ul style='list-style:none;padding:0'>{items}</ul></body></html>
    """
    return render_template_string(html)

@app.route('/list.json')
def list_json():
    images = sorted(img.name for img in OUTDIR.glob('*.png'))
    return jsonify(images)

@app.route('/plots/<path:filename>')
def plots(filename):
    return send_from_directory(OUTDIR, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
