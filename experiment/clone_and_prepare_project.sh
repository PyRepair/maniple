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
run_bgp_commands "matplotlib" 9
run_bgp_commands "matplotlib" 17
run_bgp_commands "matplotlib" 3
run_bgp_commands "matplotlib" 22
run_bgp_commands "Luigi" 4
run_bgp_commands "Luigi" 25
run_bgp_commands "Luigi" 28
run_bgp_commands "Spacy" 3
run_bgp_commands "Scrapy" 29
run_bgp_commands "Scrapy" 28
run_bgp_commands "Pandas" 30
run_bgp_commands "Pandas" 88
run_bgp_commands "Pandas" 48
run_bgp_commands "Pandas" 35
run_bgp_commands "Pandas" 122
run_bgp_commands "Pandas" 86
run_bgp_commands "Pandas" 60
run_bgp_commands "Pandas" 34
run_bgp_commands "Pandas" 129
run_bgp_commands "Pandas" 69
run_bgp_commands "Youtube-DL" 28
run_bgp_commands "Youtube-DL" 17
run_bgp_commands "Keras" 38
run_bgp_commands "Keras" 9
run_bgp_commands "Keras" 25
run_bgp_commands "Keras" 14
run_bgp_commands "Black" 10
run_bgp_commands "Black" 19
run_bgp_commands "tqdm" 4
run_bgp_commands "tornado" 14
