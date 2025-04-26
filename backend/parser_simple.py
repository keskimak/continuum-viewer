import json
import os
import requests
from fhir.resources.bundle import Bundle
from fhir.resources.medicationrequest import MedicationRequest

from typing import Dict, Any

class MedicationListParser:
    def __init__(self, file_path: str = "examples/sample_data.json"):
        self.file_path = file_path

    def parse_json_data(self) -> Dict[str, Any]:
        """
        Parse JSON data from the specified file.
        Returns the parsed data as a dictionary.
        """
        try:
            with open(self.file_path, 'r') as file:
                bundle_data = json.load(file)
                # Extract only MedicationRequest resources
                medication_requests = []
                for entry in bundle_data.get("entry"):
                    print(entry.get("resource").get("resourceType"))                    
                    if entry.get("resource").get("resourceType") == "MedicationRequest":
                        resource = entry.get("resource")
                        medication_requests.append(resource)
                        print("medication_requests added")                       
                        self.validate_resources(resource)
                
                return bundle_data
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file: {self.file_path}") 
        
    def validate_resources(self, mr):        
        FHIR_SERVER = "https://hapi.fhir.org/baseR4"
        profile_url = "http://resepti.kanta.fi/fhir/StructureDefinition/MedicationListMedicationRequest"
        response = requests.post(
            f"{FHIR_SERVER}/MedicationRequest/$validate?profile={profile_url}",
            headers={"Content-Type": "application/fhir+json"},
            json=mr
        )
        print(response.json())

