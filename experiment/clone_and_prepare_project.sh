#!/bin/bash

python3.11 bgp.py update_bug_records

# Define a function to run the bgp.py commands
run_bgp_commands() {
    project_name="$1"
    bug_id="$2"

    # Run the bgp.py commands
    python3.11 bgp.py clone --bug_list "$project_name:$bug_id"
    python3.11 bgp.py prep --bug_list "$project_name:$bug_id"
}

# Call the function manually for 30 bug records
#run_bgp_commands "matplotlib" 9
#run_bgp_commands "matplotlib" 17
#run_bgp_commands "matplotlib" 3
#run_bgp_commands "matplotlib" 22
run_bgp_commands "luigi" 4
run_bgp_commands "luigi" 25
run_bgp_commands "luigi" 28
#run_bgp_commands "spacy" 3
run_bgp_commands "scrapy" 29
run_bgp_commands "scrapy" 28
run_bgp_commands "pandas" 30
run_bgp_commands "pandas" 88
run_bgp_commands "pandas" 48
run_bgp_commands "pandas" 35
run_bgp_commands "pandas" 122
run_bgp_commands "pandas" 86
run_bgp_commands "pandas" 60
run_bgp_commands "pandas" 34
run_bgp_commands "pandas" 129
run_bgp_commands "pandas" 69
run_bgp_commands "youtube-dl" 28
run_bgp_commands "youtube-dl" 17
run_bgp_commands "keras" 38
run_bgp_commands "keras" 9
run_bgp_commands "keras" 25
run_bgp_commands "keras" 14
run_bgp_commands "black" 10
run_bgp_commands "black" 19
run_bgp_commands "tqdm" 4
run_bgp_commands "tornado" 14
