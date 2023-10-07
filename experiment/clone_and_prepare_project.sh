#!/bin/bash

# Bug records
bug_records=(
    "matplotlib 9"
    "matplotlib 17"
    "matplotlib 3"
    "matplotlib 22"
    "Luigi 4"
    "Luigi 25"
    "Luigi 28"
    "Spacy 3"
    "Scrapy 29"
    "Scrapy 28"
    "Pandas 30"
    "Pandas 88"
    "Pandas 48"
    "Pandas 35"
    "Pandas 122"
    "Pandas 86"
    "Pandas 60"
    "Pandas 34"
    "Pandas 129"
    "Pandas 69"
    "Youtube-DL 28"
    "Youtube-DL 17"
    "Keras 38"
    "Keras 9"
    "Keras 25"
    "Keras 14"
    "Black 10"
    "Black 19"
    "tqdm 4"
    "tornado 14"
)

python3.11 bgp.py update_bug_records

# Iterate over the bug records and run the commands manually
for bug_record in "${bug_records[@]}"; do
    project_name=$(echo "$bug_record" | awk '{print $1}')
    bug_id=$(echo "$bug_record" | awk '{print $2}')
    
    echo "Processing $project_name:$bug_id"
    
    # Run the bgp.py commands
    python3.11 bgp.py clone --bug_list "$project_name:$bug_id"
    python3.11 bgp.py prep --bug_list "$project_name:$bug_id"

    echo "Finished $project_name:$bug_id"
done
