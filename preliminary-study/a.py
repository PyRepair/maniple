import json
import os


# Define the directory path
dir_path = '../database/30-395-subset/bugs-info'

# Get a list of all files in the directory
files = os.listdir(dir_path)

# Iterate over each file
for file in files:
    # Check if the file is a JSON file
    if file.endswith('.json'):
        # Construct full file path
        file_path = os.path.join(dir_path, file)
        # Open the JSON file and load the data
        with open(file_path, 'r') as f:
            data = json.load(f)
        # Process the JSON data
        pn = data['project']
        for bug in data['bugs']:
            bid = bug['id']
            dirn = f"second-stratum/{pn}-{bid}"
            
            bug["project"] = pn
            with open(f"{dirn}/bug-info.json", "w") as f:
                json.dump(bug, f, indent=4)

