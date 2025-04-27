from flask import Flask, jsonify
from MedicationListParser import MedicationListParser  # <-- Your FHIR parser
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow all origins, OK for local development

PATH_TO_EXAMPLE_DATA = "examples/sample_data_filtered.json"

@app.route('/api/medication-history', methods=['GET'])
def get_medication_history():
    parser = MedicationListParser(file_path=PATH_TO_EXAMPLE_DATA)
    parser.parse_json_data(None)
    data = parser.get_grouped_by_medicine_id()
    print("data: ", data)
    return jsonify(data) 

@app.route('/api/medications', methods=['GET'])
def get_medications():
    parser = MedicationListParser(file_path=PATH_TO_EXAMPLE_DATA)
    parser.parse_json_data(None)
    data = parser.get_medication_requests()
    return jsonify(data)

@app.route('/api/continuums', methods=['GET'])
def get_continuums():
    parser = MedicationListParser(file_path=PATH_TO_EXAMPLE_DATA)
    parser.parse_json_data(None)
    continuums = parser.get_all_continuums()
    return jsonify(continuums)


if __name__ == "__main__":
    app.run(debug=True)
