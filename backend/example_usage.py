from MedicationListParser import MedicationListParser
from sample_generator import SampleGenerator


def test_sample_generator():
    print("  ")
    print("Testing sample generator")
    print("  ")
    generator = SampleGenerator()
    generator.parse_json_data()
    filtered_data = generator.return_filtered_data()
    entries = filtered_data.get("entry")
    for entry in entries:
        mr = entry.get("resource")
        for m in mr:

            # print("authoredOn: ", m.get("authoredOn"))
            print("---")
    print("Filtered data loaded successfully")


def main():
    # Create a parser instance with the default file path
    parser = MedicationListParser()
    
    # Parse the JSON data
    parser.parse_json_data(None)
    
    # Get and display medication requests
    mr = parser.get_medication_requests()
    print("Example data: Medication requests: ", len(mr))
    for m in mr:
        print("id: ", m.get("id"))
        print("medicine_id: ", m.get("medicine_id"))
        print("medicine_id_part: ", m.get("medicine_id_part"))
        print("adverse_effects: ", m.get("adverse_effects"))
        print("indications: ", m.get("indications"))
        print("authoredOn: ", m.get("authoredOn"))
        print("---")
    
    # Get and display grouped data
    grouped_by_medicine_id = parser.get_grouped_by_medicine_id()
    print("Grouped by medicine_id: ", len(grouped_by_medicine_id))
    for medicine_id, mr_list in grouped_by_medicine_id.items():
        print(f"Medicine ID: {medicine_id}")
        for mr in mr_list:
            print(f"  Medicine ID Part: {mr.get('medicine_id_part')}")
        print("---")

def test_sample_data_with_parser():
    print("  ")
    print("Testing sample data with parser")
    print("  ")
    parser = MedicationListParser(file_path="examples/sample_data_filtered.json")
    parser.parse_json_data(None)
    mr = parser.get_medication_requests()
    print("Example data: Medication requests: ", len(mr))
    for m in mr:
        print("id: ", m.get("id"))
        print("medicine_id: ", m.get("medicine_id"))
        print("medicine_id_part: ", m.get("medicine_id_part"))
        print("adverse_effects: ", m.get("adverse_effects"))
        print("indications: ", m.get("indications"))
        print("authoredOn: ", m.get("authoredOn"))
        print("---")


if __name__ == "__main__":
   # main()
    test_sample_generator()
    test_sample_data_with_parser()
