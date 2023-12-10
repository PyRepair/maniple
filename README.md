# LLM Learning to Prompt

This repository contains several experiments assessing the performance of Large Language Models (LLMs) when combining different sets of features into prompts. It focuses on understanding how different combinations of features can impact the effectiveness of prompts in eliciting accurate and relevant responses from LLMs.


## Installation

### Prerequisites
Before installing the project, ensure you have the following prerequisites installed on your system:
- Python 3.x: The script is written in Python, so you need to have Python 3.x installed. You can download it from [Python's official website](https://www.python.org/downloads/).

### Installation

Follow these steps to install and set up the project on your local machine:

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/your-username/your-repository.git
   ```
   Replace `https://github.com/your-username/your-repository.git` with the URL of your project's repository.

2. **Navigate to the Project Directory**:
   ```sh
   cd your-repository
   ```

3. **Install Dependencies**:
   If your project has external dependencies listed in a `requirements.txt` file, install them using:
   ```sh
   pip install -r requirements.txt
   ```


## Usage

This script offers a versatile command-line interface for handling a variety of tasks related to data processing and file management. Here's a detailed guide on how to use it effectively:

### Basic Command Structure
The fundamental way to use the script is as follows:
```sh
python script_name.py [command] [options]
```
Replace `script_name.py` with the actual filename of the script.

### Commands Overview
The script supports a range of commands, each designed for specific operations:

- **`prep`**: This command is used to prepare the data for subsequent processing. It sets up the necessary environment and structures to facilitate smooth data handling.

- **`extract`**: Use this command to extract crucial facts or data points from your dataset. It parses through the data to retrieve relevant information based on defined parameters.

- **`validate`**: This command is vital for ensuring the integrity and accuracy of your data. It runs checks to validate the data against certain criteria or standards.

- **`clean_feature_files` / `clean_response_files` / `clean_result_files` / `clean_log_files` / `clean_prompt_files`**: These commands are used for housekeeping purposes. They help in cleaning up various types of files, ensuring that your working environment remains organized and free of clutter.

### Options and Their Usage
The script is equipped with several options that allow for customization and flexibility:

- **`--bugids`**: Specify a comma-separated list of bug IDs for targeted processing. For instance, `--bugids pandas:30, numpy:25` would focus the script's operations on these specified bugs.

- **`--dataset`**: Choose from predefined datasets like `106subset`, `395subset`, `first-stratum`, `second-stratum`, or `all`. This option determines the scope of data the script will work on.

- **`--exclude-projects` / `--include-projects`**: These mutually exclusive options let you refine the script's focus. Use `--exclude-projects` to list projects that should be ignored during processing, and `--include-projects` for those that should be included.

- **`--output-dir`**: Define a custom directory for storing output files. This can be any path on your system where you want the script to save its results.

- **`--envs-dir`**: This option allows you to specify the path to the prepared environments, essential for running the script under certain conditions or configurations.

- **`--test-mode`**: Activate test mode with this switch. It processes only one bug from each project, useful for quick tests or demos.

- **`--overwrite`**: If set, this option allows the script to overwrite existing results, useful for updating or refreshing data outputs.

- **`--use-docker`**: Opt to run the script within a Docker container. This is particularly useful for maintaining a consistent environment, isolated from the host system.


### Data Preparation Examples
Commands for preparing data with various options:

1. **Prepare Specific Bug IDs with Custom Output Directory**
   ```sh
   python script_name.py prep --bugids pandas:30, numpy:25 --output-dir /path/to/custom/output
   ```

2. **Prepare Data Excluding Certain Projects**
   ```sh
   python script_name.py prep --dataset all --exclude-projects projectX, projectY
   ```

### Data Extraction Examples
Commands for extracting data with combined flags:

1. **Extract Data from All Datasets Using Docker**
   ```sh
   python script_name.py extract --dataset all --use-docker
   ```

2. **Extract Data in Test Mode with Specified Environment Directory**
   ```sh
   python script_name.py extract --dataset 395subset --test-mode --envs-dir /path/to/envs
   ```

### Data Validation Examples
Commands for validating data with multiple options:

1. **Validate Specific Dataset with Overwrite Enabled**
   ```sh
   python script_name.py validate --dataset 106subset --overwrite
   ```

2. **Validate Data Including and Excluding Projects**
   ```sh
   python script_name.py validate --include-projects projectA --exclude-projects projectB
   ```

### File Cleaning Examples
Examples of commands for cleaning various file types:

1. **Clean Feature Files for Specific Bug IDs in Custom Directory**
   ```sh
   python script_name.py clean_feature_files --bugids pandas:45 --output-dir /path/to/features
   ```

2. **Clean Multiple File Types for a Specific Dataset**
   ```sh
   python script_name.py clean_log_files --dataset first-stratum
   python script_name.py clean_prompt_files --dataset first-stratum
   ```

### Advanced Combination Examples
Complex commands combining multiple functionalities:

1. **Extract Data with Multiple Flags for Bug IDs, Projects, and Docker**
   ```sh
   python script_name.py extract --bugids pandas:45, scipy:20 --include-projects projectC --exclude-projects projectD --use-docker
   ```

2. **Prepare and Clean Data for Specific Dataset with Custom Environment Path**
   ```sh
   python script_name.py prep --dataset second-stratum --envs-dir /path/to/special/envs
   python script_name.py clean_response_files --dataset second-stratum --output-dir /path/to/cleanup
   ```



## Running Experiments

### Preparing Bugs

You can prepare bugs for the experiment either using Docker or the CLI. 

#### Using Docker
```bash
docker run --rm -it -v /Volumes/SSD2T/envs:/envs pyr:lite bgp prep --bugids black:10 --reinstall --separate-envs --envs-dir /envs
```

#### Using CLI
```bash
bgp prep --bugids black:10 --restart --separate-envs --envs-dir /Volumes/SSD2T/envs
```

### Extract Features

Similarly, you can extract features using Docker or the CLI.

#### Using Docker
```bash
docker run --rm -it -v /Volumes/SSD2T/envs:/envs pyr:lite bgp extract_features --bugids black:10 --separate-envs --envs-dir /envs
```

#### Using CLI
```bash
bgp extract_features --bugids black:4 --envs-dir /Volumes/SSD2T/bgp_cache
```

## Structure of Directories

The repository is structured as follows to organize the data and results of the experiments:

- `preliminary-study`: Contains data related to perfect prompts.
- `first-stratum`: Contains data from the 106 dataset, which focuses on simple bugs. Results can be found [here](https://docs.google.com/spreadsheets/d/100q3GdNcR0SfvsLZoskePINhFVXp8jx1bY5IbZzf6rs/edit?usp=sharing).
- `second-stratum`: Contains data from the 395 dataset, which includes more complex bugs.
- Files such as `preliminary-study/first-stratum/black-10/f2-1-1.md` include individual facts.

## Contributing

Contributions to this project are welcome! Please refer to our contributing guidelines for more information.

## License

This project is licensed under the [LICENSE NAME] - see the LICENSE file for details.

## Contact

For any inquiries, please reach out to [Your Name] at [Your Email].
