# Maniple

This repository contains several experiments assessing the performance of Large Language Models (LLMs) when combining different sets of features into prompts. It focuses on understanding how different combinations of features can impact the effectiveness of prompts in eliciting accurate and relevant responses from LLMs.

## Installation

Before installing the project, ensure you have the following prerequisites installed on your system:

- Python version 3.10 or higher.

Follow these steps to install and set up the project on your local machine:

```sh
python3 -m pip install .
```

## Structure of Directories

The project is organized into several directories, each serving a specific purpose:

```plaintext
data/               # Training and testing datasets
  BGP32/            # Sampled 32 bugs from the BugsInPy dataset
    black/          # The bug project folder
      10/           # The bug ID folder
        100000001/      # The bitvector used for prompting
          prompt.md         # The prompt used for this bitvector
          response_1.md     # The response from the model
          response_1.json   # The response in JSON format
          response_1.patch  # The response in patch format
          result_1.json     # Testing result
    ...
  full_dataset.txt  # Contains download link for full BGP314 dataset

maniple/            # Scripts for getting facts and generate prompts
  strata_based/     # Scripts for generating prompts
  utils/            # Utility functions
  tests/            # Test scripts
  metrics/          # Scripts for calculating metrics for dataset

experiment.ipynb    # Jupyter notebook for training models

experiment-initialization-resources/  # Contains raw facts for each bug
  bug-data/         # row facts for each bug
    ansible/        # Bug project folder
      5/            # Bug ID folder
        bug-info.json              # Metadata for the bug
        facts_in_prompt.json       # Facts used in the prompt
        processed_facts.json       # Processed facts
        external_facts.json        # GitHub issues for this bug
        static-dynamic-facts.json  # Static and dynamic facts
    ...
  datasets-list/    # Subsets from BugsInPy dataset
  strata-bitvector/ # Debugging information for bitvectors
```

## Fact Extraction

The CLI scripts under the `maniple` directory provide useful commands to prepare environments for each bug and extract facts from the bug data.

In order to prepare the environments for each bug, you can use the `prep` command as follows:

```sh
maniple prep --bugids black:10
```

This script will automatically download black repository from GitHub, create a virtual environment for the bug with id 10 and install the necessary dependencies. Replace `black:10` with the bug id you want to prepare.

Then you can extract facts from the bug data using the `extract` command as follows:

```sh
maniple extract --bugids black:10 --output-dir /path/to/output
```

This script will extract facts from the bug data and save them in the specified output directory.

You can find all extracted facts under the `experiment-initialization-resources/bug-data` directory.

## Generate Bitvector Specific Prompts and Responses

Please use following command:

```sh
python3 -m maniple.strata_based.prompt_generator --database 314-dataset --partition 10 --start_index 1 --trial 15
```

This script will generate prompts and responses for all 314 bugs in the dataset by enumerating all possible bitvectors according to current strata design specified in `maniple/strata_based/fact_strata_table.json`. By specifying `--trial 15`, the script will generate 15 responses for each prompt. And by specifying `--partition 10` the script will start 10 threads to speed up the process.

## Testing Generated Patches

Please use following command:

```sh
maniple validate --bugids black:10 --output-dir /path/to/output
```

This script will validate the generated patches for the specified bug and save the results in the specified output directory.

## Contributing

Contributions to this project are welcome! Please submit a PR if you find any bugs or have any suggestions.

## License

This project is licensed under the MIT - see the LICENSE file for details.
