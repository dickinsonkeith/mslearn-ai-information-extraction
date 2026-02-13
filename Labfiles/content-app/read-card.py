def analyze_card(image_file, analyzer, endpoint, key):
    # Everything below is now properly indented
    print(f"Analyzing {image_file}")

    # Set the API version
    CU_VERSION = "2025-05-01-preview"

    # Read the image data
    try:
        with open(image_file, "rb") as file:
            image_data = file.read()
    except FileNotFoundError:
        print(f"Error: The file {image_file} was not found.")
        return

    # Use a POST request to submit the image data
    print("Submitting request...")
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/octet-stream"
    }
    url = f'{endpoint}/contentunderstanding/analyzers/{analyzer}:analyze?api-version={CU_VERSION}'
    
    response = requests.post(url, headers=headers, data=image_data)
    
    if response.status_code != 202:
        print(f"Failed to submit: {response.status_code} - {response.text}")
        return

    # Extract the operation ID from headers or body
    # Azure Content Understanding usually returns the operation-location URL in headers
    # but based on your code, we'll check the response body for an ID
    response_json = response.json()
    id_value = response_json.get("id")

    # Use a GET request to check the status
    print('Getting results...')
    result_url = f'{endpoint}/contentunderstanding/analyzerResults/{id_value}?api-version={CU_VERSION}'
    
    while True:
        result_response = requests.get(result_url, headers=headers)
        result_json = result_response.json()
        status = result_json.get("status")

        print(f"Status: {status}")

        if status == "Succeeded":
            break
        elif status == "Failed":
            print("Analysis failed.")
            return
        
        time.sleep(2) # Wait before polling again

    # Process the analysis results
    print("Analysis succeeded:\n")
    output_file = "results.json"
    with open(output_file, "w") as json_file:
        json.dump(result_json, json_file, indent=4)
        print(f"Response saved in {output_file}\n")

    # Extract the fields
    contents = result_json.get("result", {}).get("contents", [])
    for content in contents:
        fields = content.get("fields", {})
        for field_name, field_data in fields.items():
            # Mapping types to their specific value keys
            value_mapping = {
                "string": "valueString",
                "number": "valueNumber",
                "integer": "valueInteger",
                "date": "valueDate",
                "time": "valueTime",
                "array": "valueArray"
            }
            
            f_type = field_data.get('type')
            val_key = value_mapping.get(f_type)
            if val_key and val_key in field_data:
                print(f"{field_name}: {field_data[val_key]}")
