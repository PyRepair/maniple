# LLM Learning to Prompt
This repository contains several experiments how accessing the performance of LLM when combining different set of features into prompts.

## Setup the experiment environment

Build the docker container first. You can add optional argument `--progress=plain` to see the progress of building.

```bash
cd experiment
docker build -t ubuntu-python-env .
```

Switch to your local host directory and clone the GitHub repository

```bash
cd <directory-for-git-repos>
git clone https://github.com/PyRepair/PyRepair.git
```

Run the docker container and bind the volume to your local directory

```bash
docker run -it -v <directory-to-pyrepair-git-repo>:/data ubuntu-python-env
```

Now we have entered the experiment environment. Before running the script, we need to install the dependencies.

```bash
cd /data
python3.11 -m pip install -r requirements.txt
cd benchmark_wrangling/BugsInPy
python3.11 -m pip install -r requirements.txt
```

After installing the dependencies, we finish the environment setup.

## Extracting errors and stack traces from BugsInPy

First we need to update bug repository registration from the BugsInPy project.

```bash
python3.11 bgp.py update_bug_records
```

Use following commands to `clone`, `prep` and `run_test` for each bug repository.
```bash
python3.11 bgp.py clone —bug_list <project name>:<id>
python3.11 bgp.py prep —bug_list <project name>:<id>
python3.11 bgp.py run_test —bug_list <project name>:<id>
```

## Build prompt and run result generator for prompt
```bash
cd experiment
python3.8 llm_repair.py -d <dataset> -p <project> -t <0|1> -f <0|1> -m <llm model name> -r 3
```
Explaination:
```bash
python llm_repair.py -d <dataset> -p <project> -t <0|1> (0 : single prompt type, 1 : multi prompt type) -f <0|1> (0 : use all features, 1 : traversal all features drop one feature every run) -m <llm model name> -r 3 (how many answers are generated from prompt)
```
Example:
```bash
python llm_repair.py -d "106-subset" -p tornado -t 0 -f 0 -m gpt-3.5-turbo -r 3
```



# Relevant docs

- [Project Planning (Google Doc)](https://docs.google.com/document/d/1XVV7IkuQQ8rD3oK32kgK2NNJ0A5LC93uxbUYW7T9TGg/edit?usp=sharing)
- [Result Spreadsheet for manually selected bugs (Google Sheet)](https://docs.google.com/spreadsheets/d/1XYWpsnhUVL7p8IS9K6jc1vadp2cirJ5O7VIA-F8hCH8/edit?usp=sharing)
- [Result Spreadsheet for random selected 30 bugs in 106 subset in bgp](https://docs.google.com/spreadsheets/d/1YBWC5g7Or081PAXBJg5UFxidwlLGj6hWCl7MMVbrugo/edit?usp=sharing)
- [Result Spreadsheet for random selected 30 bugs in 395 subset in bgp](https://docs.google.com/spreadsheets/d/100q3GdNcR0SfvsLZoskePINhFVXp8jx1bY5IbZzf6rs/edit?usp=sharing)
