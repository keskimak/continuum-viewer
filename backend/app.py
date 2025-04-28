from flask import Flask, jsonify
from MedicationListParser import MedicationListParser  # <-- Your FHIR parser
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # local development purposes

# TODO: move to config
PATH_TO_EXAMPLE_DATA = "examples/sample_data_filtered.json"

# TODO: api address to config
@app.route('/api/medication-history', methods=['GET'])
def get_medication_history():
    parser = MedicationListParser(file_path=PATH_TO_EXAMPLE_DATA)
    parser.parse_json_data(None)
    data = parser.get_laakityslista()
    print("data: ", data)
    return jsonify(data) 

if __name__ == "__main__":
    app.run(debug=True)
