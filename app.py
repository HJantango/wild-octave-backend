from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# This enables CORS for all domains on all routes.
CORS(app)

@app.route('/')
def hello_world():
    # A simple route to confirm the server is running.
    return 'Hello from the Wild Octave Organics Backend!'

@app.route('/extract', methods=['POST'])
@cross_origin() # This is an extra measure to ensure CORS is handled for this route
def extract_data():
    # Basic check to ensure a file was uploaded.
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # --- MOCK EXTRACTION LOGIC ---
    # This is our placeholder data. In the future, this section will be replaced
    # with real logic to parse the uploaded file.
    mock_data = {
        "vendor": "Mock Supplier Inc.",
        "items": [
            {"item_name": "Organic Bananas", "cost_ex_gst": "15.50", "units": "1kg", "unit_price": None},
            {"item_name": "Almond Milk 1L", "cost_ex_gst": "24.00", "units": "6 units", "unit_price": "4.00"},
            {"item_name": "Protein Powder 500g", "cost_ex_gst": "35.00", "units": "1 unit", "unit_price": "35.00"}
        ]
    }
    
    # This is the corrected line. It sends the entire mock_data object.
    return jsonify(mock_data)

if __name__ == "__main__":
    # This part is for local development and not used by Render, but it's good practice.
    app.run(debug=True)
