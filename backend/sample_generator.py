import json
import random
from datetime import datetime, timedelta
from extension_urls import MEDICATION_REQUEST_EXTENSIONS,get_extension_url
from MedicationListParser import MedicationListParser

class SampleGenerator:
    def __init__(self, file_path: str = "examples/sample_data.json"):
        self.file_path = file_path
        self.filtered_data = None

    def return_filtered_data_from_file(self):
        with open("examples/sample_data_filtered.json", 'r') as file:
            return json.load(file)
        
    def return_filtered_data(self):
        return self.filtered_data


    def parse_json_data(self):
        """
        Parse JSON data from the specified file.
        Returns the parsed data as a dictionary.
        """
        try:
            with open(self.file_path, 'r') as file:
                
                bundle_data = json.load(file)
                # Filter out MedicationDispense entries from the bundle data
                if "entry" in bundle_data:
                    bundle_data["entry"] = [
                        entry for entry in bundle_data["entry"] 
                        if is_medication_request(entry)
                    ]
                parser = MedicationListParser(bundle_data)
                parser.parse_json_data(bundle_data)
                print("Entries: ",len(bundle_data["entry"]))
                print("Total: ", str (bundle_data["total"]))
                if int(bundle_data["total"]) != len(bundle_data["entry"]):
                    bundle_data["total"] = len(bundle_data["entry"])
                    print("Updated Total: " + str (bundle_data["total"]))
                    for entry in bundle_data["entry"]:
                        print("ID: ",entry.get("resource").get("id"))
                        print("Authored On: ",entry.get("resource").get("authoredOn"))
                        if entry.get("resource").get("authoredOn") is None:
                            # Example usage
                            start_date = datetime(2020, 1, 1)
                            end_date = datetime(2024, 12, 31)

                            rand_dt = random_datetime(start_date, end_date)
                            print(rand_dt)
                            entry["resource"]["authoredOn"] = rand_dt
                            print("Updated Authored On: ",entry.get("resource").get("authoredOn"))
                        print("--------------------------------")
                self.filtered_data = bundle_data
            with open("examples/sample_data_filtered.json", "w") as file:
                json.dump(bundle_data, file, indent=4)
            self.filtered_data = bundle_data
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
            return None




@staticmethod
def is_medication_request(entry) -> bool:
    return entry.get("resource", {}).get("resourceType") == "MedicationRequest"

def insert_adverse_effects(entry):
    extension_dict =MedicationListParser.build_extension_dict(entry)
    adverse_effects = extension_dict.get(MEDICATION_REQUEST_EXTENSIONS.get("ADVERSE_EFFECTS"))
    if adverse_effects is None:
        print("Adverse effects not found")
        entry["resource"]["extension"].append(adverse_effects)
    return entry


def random_datetime(start, end):
    """
    Generate a random datetime between two datetime objects.
    """
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    rand_dt = start + timedelta(seconds=random_seconds)
    formatted_dt = rand_dt.strftime("%m/%d/%Y %H:%M:%S")
    return formatted_dt


adverse_effects = {
                        "url": "http://resepti.kanta.fi/fhir/StructureDefinition/extension/adverseEffect",
                        "valueCoding": {
                            "code": "G43.9#",
                            "system": "urn:oid:1.2.246.537.6.1.1999"
                        }
                    }


indication = {
                        "url": "http://resepti.kanta.fi/fhir/StructureDefinition/extension/structuredIndication",
                        "valueCoding": {
                            "code": "J06.9",
                            "system": "urn:oid:1.2.246.537.6.1.1999"
                        }
                    }
