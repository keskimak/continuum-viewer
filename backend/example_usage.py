from parser_simple import MedicationListParser

def main():
    # Create a parser instance with the default file path
    parser = MedicationListParser()
    
    # Parse the JSON data
    data = parser.parse_json_data()
    print("Parsed JSON data:")
    
    # Get a summary of the data
    summary = parser.get_data_summary()
    print("\nData summary:")
    print(summary)
    
    # Get the items
    items = parser.get_items()
    print("\nItems:")
    for item in items:
        print(f"- {item['name']} (ID: {item['id']}, Status: {item['status']}, Progress: {item['progress']}%)")
    
    # Get the metadata
    metadata = parser.get_metadata()
    print("\nMetadata:")
    print(metadata)

if __name__ == "__main__":
    main() 