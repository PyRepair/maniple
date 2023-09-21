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

# Relevant docs

- [Project Planning (Google Doc)](https://docs.google.com/document/d/1XVV7IkuQQ8rD3oK32kgK2NNJ0A5LC93uxbUYW7T9TGg/edit?usp=sharing)
- [Result Spreadsheet (Google Sheet)](https://docs.google.com/spreadsheets/d/1XYWpsnhUVL7p8IS9K6jc1vadp2cirJ5O7VIA-F8hCH8/edit?usp=sharing)
