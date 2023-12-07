import json
import os.path
import random


def save_bitvector(filename: str, bitvector: dict):
    with open(filename, "w") as f:
        json.dump(bitvector, f, indent=4)


fact_bitvector = {
    "1": {
        "1.1.1": 1,
        "1.1.2": 1
    },
    "2": {
        "1.2.1": 1,
        "1.2.2": 1,
        "1.2.3": 1
    },
    "3": {
        "1.3.1": 1,
        "1.3.2": 1
    },
    "4": {
        "1.4.1": 1,
        "1.4.2": 1,
        "2.1.1": 1,
        "2.1.2": 1
    },
    "5": {
        "2.1.3": 1,
        "2.1.4": 1
    },
    "6": {
        "2.1.5": 1,
        "2.1.6": 1
    },
    "7": {
        "3.1.1": 1,
        "3.1.2": 1
    },
    "8": {
        "cot": 1
    }
}


save_bitvector(os.path.join("..", "preliminary-study", "all_facts_bitvector.json"), fact_bitvector)
num_samples = 5

for i in range(num_samples):
    for fact_class in fact_bitvector.keys():
        if fact_class == "5" or fact_class == "6":
            continue

        fact_strata: dict = fact_bitvector[fact_class]
        if random.randint(0, 1) == 1:
            for fact_label in fact_strata.keys():
                fact_strata[fact_label] = 1
        else:
            for fact_label in fact_strata.keys():
                fact_strata[fact_label] = 0

    select_5 = random.randint(0, 1)
    select_6 = random.randint(0, 1)
    while select_5 == 1 and select_6 == 1:
        select_5 = random.randint(0, 1)
        select_6 = random.randint(0, 1)

    fact_strata = fact_bitvector["5"]
    for fact_label in fact_strata.keys():
        fact_strata[fact_label] = select_5

    fact_strata = fact_bitvector["6"]
    for fact_label in fact_strata.keys():
        fact_strata[fact_label] = select_6

    save_bitvector(os.path.join("..", "preliminary-study", "random_sampled_facts_bitvector_" + str(i + 1) + ".json"),
                   fact_bitvector)
