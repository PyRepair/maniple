import json
import os.path
import random


def save_bitvector(filename: str, bitvector: dict):
    with open(filename, "w") as f:
        json.dump(bitvector, f, indent=4)


def generate_binary_codes(digit_length):
    all_codes = []
    for index in range(2 ** digit_length):
        all_codes.append([int(digit) for digit in bin(index)[2:].zfill(n)])
    return all_codes


strata_bitvector = {
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
        "2.1.4": 1,
        "2.1.5": 1,
        "2.1.6": 1
    },
    "6": {
        "3.1.1": 1,
        "3.1.2": 1
    },
    "7": {
        "cot": 1
    }
}

database_path = os.path.join("..", "preliminary-study", "strata-bitvectors")

if not os.path.exists(database_path):
    os.makedirs(database_path)


# "traversal" or "random"
mode = "traversal"

if mode == "random":
    num_samples = 5
    for i in range(num_samples):
        code = ""
        for fact_class in strata_bitvector.keys():
            if fact_class == "1":
                continue

            fact_strata: dict = strata_bitvector[fact_class]
            select = random.randint(0, 1)
            if select == 1:
                for fact_label in fact_strata.keys():
                    fact_strata[fact_label] = 1
            else:
                for fact_label in fact_strata.keys():
                    fact_strata[fact_label] = 0

            code += str(select)

        save_bitvector(os.path.join(database_path, f"{code}_bitvector.json"),
                       strata_bitvector)

else:
    n = 6
    codes = generate_binary_codes(n)

    for code in codes:
        bitvector = strata_bitvector
        for index in range(len(code)):
            facts: dict = bitvector[str(index + 1)]
            for fact in facts.keys():
                facts[fact] = code[index]

        code_str = ''.join(map(str, code))
        save_bitvector(os.path.join(database_path, f"{code_str}_bitvector.json"),
                       strata_bitvector)
