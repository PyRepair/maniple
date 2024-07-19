import itertools

# Define the parts
part1 = "h"
part2 = "e"
part3 = "l"
part4 = "l"
part5 = "o"

fact_group_permutation = "12345"

# Create a list of parts
parts = [part1, part2, part3, part4, part5]

# Generate all permutations
permutations = list(itertools.permutations(parts))

# Get a specific permutation (for example, the 3rd one)
print(len(permutations))

for i in range(len(permutations)):

    # Join the permutation into a string
    result = ''.join(permutations[i])

    print(f"The permutation {i} is:", result)