import json
import random


def save_bitvector(filename: str, fact_bitvector: dict):
    with open(filename, "w") as f:
        json.dump(fact_bitvector, f, indent=4)


bitvector = {
    "1.3.2": 1,
    "1.2.4": 1,
    "1.2.1": 1,
    "1.3.4": 1,
    "2.1.1": 1,
    "2.1.2": 1,
    "2.2.1": 1,
    "2.2.2": 1,
    "3.1.1": 1,
    "3.1.2": 1,
    "cot": 1
}

save_bitvector("all_facts_bitvector.json", bitvector)

for i in range(5):
    for key in bitvector:
        bitvector[key] = random.randint(0, 1)
    save_bitvector("random_sampled_facts_bitvector" + str(i) + ".json", bitvector)
