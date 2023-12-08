# LLM Learning to Prompt
This repository contains several experiments how accessing the performance of LLM when combining different set of features into prompts.

## Running experiment

### Preparing bugs

Using docker
```bash
docker run --rm -it -v /Volumes/SSD2T/envs:/envs pyr:lite bgp prep --bugids black:10 --reinstall --separate-envs --envs-dir /envs
```

Using CLI
```bash
bgp prep --bugids black:10 --restart --separate-envs --envs-dir /Volumes/SSD2T/envs
```

### Extract features

Using docker
```bash
docker run --rm -it -v /Volumes/SSD2T/envs:/envs pyr:lite bgp extract_features --bugids black:10 --separate-envs --envs-dir /envs
```

Using CLI
```bash
bgp extract_features  --bugids black:4 --envs-dir /Volumes/SSD2T/bgp_cache
```


# Structure of Directories

`preliminary-study` contains data related to perfect prompts.

`first-stratum` is from 106 dataset (simple bugs); results: https://docs.google.com/spreadsheets/d/100q3GdNcR0SfvsLZoskePINhFVXp8jx1bY5IbZzf6rs/edit?usp=sharing
`second-stratum` is from the 395 dataset (complex bugs): 

Files like `preliminary-study/first-stratum/black-10/f2-1-1.md' include individual facts.

