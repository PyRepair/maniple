import json
import os.path
import random


def save_bitvector(filename: str, fact_bitvector: dict):
    with open(filename, "w") as f:
        json.dump(fact_bitvector, f, indent=4)


bitvector: dict = {
    "1.3.1": 1,
    "1.3.2": 1,
    "1.2.1": 1,
    "1.2.2": 1,
    "1.2.3": 1,
    "1.1.2": 1,
    "2.2.3": 1,
    "2.2.4": 1,
    "2.2.5": 1,
    "2.2.6": 1,
    "2.1.1": 1,
    "2.1.2": 1,
    "2.2.1": 1,
    "2.2.2": 1,
    "3.1.1": 1,
    "3.1.2": 1,
    "cot": 1
}


save_bitvector(os.path.join("..", "preliminary-study", "all_facts_bitvector.json"), bitvector)
num_samples = 5

for i in range(num_samples):
    bitvector["1.3.1"] = random.randint(0, 1)
    bitvector["1.3.2"] = random.randint(0, 1)
    bitvector["1.2.1"] = random.randint(0, 1)

    # only sample class docs if class declaration is selected
    if bitvector["1.2.1"] == 1:
        bitvector["1.2.2"] = random.randint(0, 1)
    else:
        bitvector["1.2.2"] = 0

    bitvector["1.2.3"] = random.randint(0, 1)
    bitvector["1.1.2"] = random.randint(0, 1)

    bitvector["2.2.3"] = random.randint(0, 1)
    bitvector["2.2.4"] = random.randint(0, 1)
    bitvector["2.2.5"] = random.randint(0, 1)
    bitvector["2.2.6"] = random.randint(0, 1)

    bitvector["2.1.1"] = random.randint(0, 1)
    # only sample test file name if test code is provided
    if bitvector["2.1.1"] == 1:
        bitvector["2.1.2"] = random.randint(0, 1)
    else:
        bitvector["2.1.2"] = 0

    bitvector["2.2.1"] = random.randint(0, 1)
    bitvector["2.2.2"] = random.randint(0, 1)
    bitvector["3.1.1"] = random.randint(0, 1)
    bitvector["3.1.2"] = random.randint(0, 1)

    save_bitvector(os.path.join("..", "preliminary-study", "random_sampled_facts_bitvector" + str(i) + ".json"),
                   bitvector)
