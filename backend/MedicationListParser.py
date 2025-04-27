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
        self.grouped_by_medicine_id = []
        self.grouped_by_medicine_id_and_medicine_id_part = []

    def get_medication_requests(self):
        return self.medication_requests
    
    def get_grouped_by_medicine_id(self):
        print("Grouped by medicine id: ", self.grouped_by_medicine_id)
        return self.grouped_by_medicine_id
    
    def get_grouped_by_medicine_id_and_medicine_id_part(self):
        return self.grouped_by_medicine_id_and_medicine_id_part
    
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
                
            lists = []
            medication_requests = []
            
            # Extract only MedicationRequest resources
            medication_requests = []
            for entry in bundle_data.get("entry"):
                if entry.get("resource").get("resourceType") == "List":
                    lists.append(entry.get("resource"))
 
                    
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
                                medicine_id = medicine_id.replace("urn:oid:", "")
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
                    print("Medication request added: ", mr_id, medicine_id, medicine_id_part)

                    # self.validate_resources(resource)
            print("Parser: Medication requests: ", len(medication_requests))       
            self.medication_requests = medication_requests
            self.group_medication_requests()
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
            
            
            
    def validate_resources(self, mr):        
        response = requests.post(
            f"{FHIR_SERVER_BASE}/MedicationRequest/$validate?profile={MEDICATION_LIST_PROFILE}",
            headers={"Content-Type": "application/fhir+json"},
            json=mr
        )
        print(response.json())

    def get_all_continuums(self):
        return [continuum.to_dict() for continuum in self.continuums]
    
    def group_medication_requests(self):
        print("Grouping medication requests")
        # Step 1: Group by medicineId
        medicines = {}  # medicineId -> MedicineInUse
        continuums = []
        medication_requests = self.get_medication_requests()
        for mr in medication_requests:
            print("Grouping medication request: ", mr.get("id"))
            # Assume continuum info is inside extensions or attributes
            med_id = mr.get('medicine_id')  # eg. urn:oid:1.2.246.10.11111111.93001.2024.12345678
            med_part = mr.get('medicine_id_part')  # eg. 9876543210
            print("med_id: ", med_id)
            if med_id is None or med_part is None:
                continue  # skip if missing

            # Create MedicineInUse if not already created
            if med_id not in medicines:
                medicine = {
                    "medicine_id": med_id,
                    "continuums": []
                }
                print("medicineinuse created")
                medicines[med_id] = medicine

            else:
                medicine = medicines[med_id]

            # Find matching Continuum by medicineIdPart
            continuum = next((c for c in medicine.get("continuums") if c.get("medicine_id_part") == med_part), None)

            if continuum is None:
                continuum = {
                    "medicine_id_part": med_part,
                    "medication_requests": []
                }
                print("continuum created")
                medicine.get("continuums").append(continuum)
                continuums.append(continuum)

            continuum.get("medication_requests").append(mr)

        self.grouped_by_medicine_id = list(medicines.values())  # list of MedicineInUse objects
        self.continuums = continuums

class Continuum:
    all_instances = []  # Class variable to store all instances

    def __init__(self):
        self.medicine_id_part = None
        self.medication_requests = []
        Continuum.all_instances.append(self)  # Add this instance to the list

    @classmethod
    def get_all_instances(cls):
        return cls.all_instances

    def add_medication(self, medication_request):
        self.medication_requests.append(medication_request)
        
    def to_dict(self):
        return {
            "medicine_id_part": self.medicine_id_part,
            "medication_requests": self.medication_requests,
            # add other fields as needed
        }

class MedicineInUse:
    def __init__(self):
        self.medicine_id = None
        self.continuums = []
        
    def add_continuum(self, continuum):
        self.continuums.append(continuum)
        
    def get_continuums(self):
        return self.continuums
    
    def to_dict(self):
        return {
            "medicine_id": self.medicine_id,
            "continuums": [continuum.to_dict() for continuum in self.continuums]
        }
        
class MedicationList:
    def __init__(self):
        self.medicationlist = []
        
    def add_medication_in_use(self, medication_in_use):
        self.medicationlist.append(medication_in_use)
        
    def get_medicationlist(self):
        return self.medicationlist
        
        
