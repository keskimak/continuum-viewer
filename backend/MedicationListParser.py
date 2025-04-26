import json
import os
import requests
from fhir.resources.bundle import Bundle
from fhir.resources.medicationrequest import MedicationRequest
from extension_urls import get_extension_url, FHIR_SERVER_BASE, MEDICATION_LIST_PROFILE, MEDICATION_REQUEST_EXTENSIONS

from typing import Dict, Any

class MedicationListParser:
    def __init__(self, file_path: str = "examples/sample_data.json"):
        self.file_path = file_path
        self.medication_requests = []
        self.continuums = []
        
    def get_medication_requests(self):
        return self.medication_requests
    
    def parse_json_data(self, data):
        """
        Parse JSON data from the specified file.
        Returns the parsed data as a dictionary.
        """
        try:
            
            if data is None:
                with open(self.file_path, 'r') as file:
                    print("Parsing JSON data from file: ", self.file_path)
                    bundle_data = json.load(file)
            else:
                bundle_data = data

            # Extract only MedicationRequest resources
            medication_requests = []
            for entry in bundle_data.get("entry"):
                if entry.get("resource").get("resourceType") == "MedicationRequest":
                    mr = entry.get("resource")
                    mr_id = mr.get("id")
                    print("Medication request id: ", mr_id)
                    medicine_id = None
                    medicine_id_part = None
                    adverse_effects = []
                    indications = []
                    # Build extension dictionary for easier access
                    ext_dict = self.build_extension_dict(mr)
                    # Group by medicine id and medicine id part
                    continuum_extension = ext_dict.get(MEDICATION_REQUEST_EXTENSIONS.get("CONTINUUM"))
                    if continuum_extension:
                        nested_extension = continuum_extension.get("extension")
                        for ext in nested_extension:
                            if ext.get("url") == MEDICATION_REQUEST_EXTENSIONS.get("MEDICINE_ID"):
                                medicine_id = ext.get("valueIdentifier").get("value")
                            if ext.get("url") == MEDICATION_REQUEST_EXTENSIONS.get("MEDICINE_ID_PART"):
                                medicine_id_part = ext.get("valuePositiveInt")
                    
                    adverse_effect_ext = ext_dict.get(MEDICATION_REQUEST_EXTENSIONS.get("ADVERSE_EFFECTS"))
                    if adverse_effect_ext:
                        adverse_effects.append(adverse_effect_ext.get("valueCoding"))

                    indication_ext = ext_dict.get(MEDICATION_REQUEST_EXTENSIONS.get("INDICATIONS"))
                    if indication_ext:
                        indications.append(indication_ext.get("valueCoding"))
                            
                            
                    medication_requests.append({
                        "id": mr_id,
                        "medicine_id": medicine_id,
                        "medicine_id_part": medicine_id_part,
                        # Add authored on date for sorting
                        "authored_on": mr.authoredOn if hasattr(mr, "authoredOn") else None,
                        # FHIR resource
                        "medication_request": mr,
                        "adverse_effects": adverse_effects,
                        "indications": indications
                    })

                    # self.validate_resources(resource)
            print("Parser: Medication requests: ", len(medication_requests))       
            self.medication_requests = medication_requests
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file: {self.file_path}") 
        
    @staticmethod
    def build_extension_dict(resource):
        """Create a dictionary of extensions keyed by URL. for easier access"""
        extension_dict = {}
        for ext in resource.get("extension") or []:
            extension_dict[ext.get("url")] = ext
        return extension_dict
    
    def get_grouped_by_medicine_id(self):
        medication_requests = self.get_medication_requests()
        grouped_by_medicine_id = {}
        for mr in medication_requests:
            medicine_id = mr.get("medicine_id")
            if medicine_id not in grouped_by_medicine_id:
                grouped_by_medicine_id[medicine_id] = []
            grouped_by_medicine_id[medicine_id].append(mr)
        return grouped_by_medicine_id

    def get_grouped_by_medicine_id_and_medicine_id_part(self):
        medication_requests = self.get_medication_requests()
        grouped_by_medicine_id_and_medicine_id_part = {}
        for mr in medication_requests:
            medicine_id = mr.get("medicine_id")
            medicine_id_part = mr.get("medicine_id_part")
            if medicine_id not in grouped_by_medicine_id_and_medicine_id_part:
                grouped_by_medicine_id_and_medicine_id_part[medicine_id] = {}
            if medicine_id_part not in grouped_by_medicine_id_and_medicine_id_part[medicine_id]:
                grouped_by_medicine_id_and_medicine_id_part[medicine_id][medicine_id_part] = []
            grouped_by_medicine_id_and_medicine_id_part[medicine_id][medicine_id_part].append(mr)
        return grouped_by_medicine_id_and_medicine_id_part
            
            
            
            
    def validate_resources(self, mr):        
        response = requests.post(
            f"{FHIR_SERVER_BASE}/MedicationRequest/$validate?profile={MEDICATION_LIST_PROFILE}",
            headers={"Content-Type": "application/fhir+json"},
            json=mr
        )
        print(response.json())
