import pstats

# Define a function to create a textual description of the call graph
def create_textual_call_graph(profile_file):
    stats = pstats.Stats(profile_file)
    descriptions = []

    for func, (_, _, _, _, callers) in stats.stats.items():
        func_name = func[-1]  # get the function name
        callers_names = [caller[-1] for caller in callers.keys()]  # get the callers' function names
        description = f"The function '{func_name}' is called by: {', '.join(callers_names)}"
        descriptions.append(description)

    return "\n".join(descriptions)

# Use the function to create the textual call graph
textual_call_graph = create_textual_call_graph('program.prof')

# Print the textual call graph
print(textual_call_graph)
