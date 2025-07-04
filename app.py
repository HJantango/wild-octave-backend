# app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import pytesseract
from PIL import Image
import pandas as pd

app = Flask(__name__)
CORS(app)

from flask_cors import CORS
CORS(app)

@app.route("/")
def home():
    return "Wild Octave Backend is running!"

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/extract', methods=['POST'])
def extract():
    file = request.files['file']
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)

    ext = file.filename.lower().split('.')[-1]
    items = []

    if ext in ['pdf']:
        with pdfplumber.open(filename) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    # Skip header row, flatten rest
                    for row in table[1:]:
                        items.append({'raw': row})
    elif ext in ['jpg', 'jpeg', 'png']:
        image = Image.open(filename)
        text = pytesseract.image_to_string(image)
        # Very basic: split lines, you’ll want to improve this!
        for line in text.splitlines():
            if line.strip():
                items.append({'raw': line.strip()})
    elif ext in ['xlsx', 'xls']:
        df = pd.read_excel(filename)
        for _, row in df.iterrows():
            items.append({'raw': row.to_dict()})
    elif ext == 'csv':
        df = pd.read_csv(filename)
        for _, row in df.iterrows():
            items.append({'raw': row.to_dict()})
    else:
        return jsonify({'error': 'Unsupported file type'}), 400

    os.remove(filename)
    return jsonify({'items': items})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
