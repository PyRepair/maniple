def generate_variable_angelic_info(facts: dict, bitvector: dict = None) -> str:
    content = ""
    if bitvector is None:
        bitvector = {
            "2.3.1": 1,
            "2.3.2": 1
        }
    
    variable_angelic_value_test_cases: list = facts["2.3.1"]
    variable_angelic_type_test_cases: list = facts["2.3.2"]

    place_holder = ""
    if bitvector["2.3.1"] == 1 and bitvector["2.3.2"] == 1:
        place_holder = "values and types"
    elif bitvector["2.3.1"] == 1:
        place_holder = "values"
    elif bitvector["2.3.2"] == 1:
        place_holder = "types"

    content = content + f"## Expected {place_holder} of variables during the failing test execution\n"
    content = content + f"Each case below includes input parameter {place_holder}, and the expected {place_holder} of relevant variables at the function's return. If an input parameter is not reflected in the output, it is assumed to remain unchanged. A corrected function must satisfy all these cases.\n\n"

    for test_case_index in range(len(variable_angelic_value_test_cases)):
        content = content + f"### Expected case {test_case_index + 1}\n"

        angelic_values: list = variable_angelic_value_test_cases[test_case_index]
        angelic_types: list = variable_angelic_type_test_cases[test_case_index]

        content = content + f"#### The {place_holder} of buggy function's parameters\n"

        input_parameter_values: dict = angelic_values[0]
        input_parameter_types: dict = angelic_types[0]

        content = create_angelic_content_filed(bitvector, content, input_parameter_types, input_parameter_values)

        variable_values_before_return: dict = angelic_values[1]
        variable_types_before_return: dict = angelic_types[1]
        if len(variable_values_before_return) > 0:
            content = content + f"#### Expected {place_holder} of variables right before the buggy function's return\n"

            content = create_angelic_content_filed(bitvector, content, variable_types_before_return, variable_values_before_return)
    
    return content


def create_angelic_content_filed(bitvector, content, variable_types_before_return, variable_values_before_return):
    for variable in variable_values_before_return.keys():
        variable_value = variable_values_before_return[variable]["value"]
        variable_type = variable_types_before_return[variable]
        if variable_values_before_return[variable]["omitted"]:
            variable_shape = f", shape: `{variable_values_before_return[variable]['shape']}`"
        else:
            variable_shape = ""

        content = content + f"{variable}, "

        if bitvector["2.3.1"] == 1 and bitvector["2.3.2"] == 1:
            content = content + f"expected value: `{variable_value}`{variable_shape}, type: `{variable_type}`"
        elif bitvector["2.3.1"] == 1:
            content = content + f"expected value: `{variable_value}`{variable_shape}"
        elif bitvector["2.3.2"] == 1:
            content = content + f"expected type: `{variable_type}`"

        content = content + "\n\n"
    return content


def generate_variable_runtime_info(facts: dict, bitvector: dict = None) -> str:
    content = ""
    if bitvector is None:
        bitvector = {
            "2.2.1": 1,
            "2.2.2": 1
        }
    
    variable_runtime_value_test_cases: list = facts["2.2.1"]
    variable_runtime_type_test_cases: list = facts["2.2.2"]

    place_holder = ""
    if bitvector["2.2.1"] == 1 and bitvector["2.2.2"] == 1:
        place_holder = "values and types"
    elif bitvector["2.2.1"] == 1:
        place_holder = "values"
    elif bitvector["2.2.2"] == 1:
        place_holder = "types"

    content = content + f"## Runtime {place_holder} of variables inside the buggy function\n"

    content = content + f"Each case below includes input parameter {place_holder}, and the {place_holder} of relevant variables at the function's return, derived from executing failing tests. If an input parameter is not reflected in the output, it is assumed to remain unchanged. Note that some of these values at the function's return might be incorrect. Analyze these cases to identify why the tests are failing to effectively fix the bug.\n\n"

    for test_case_index in range(len(variable_runtime_value_test_cases)):
        content = content + f"### Case {test_case_index + 1}\n"

        runtime_values: list = variable_runtime_value_test_cases[test_case_index]
        runtime_types: list = variable_runtime_type_test_cases[test_case_index]

        content = content + f"#### Runtime {place_holder} of the input parameters of the buggy function\n"

        input_parameter_values: dict = runtime_values[0]
        input_parameter_types: dict = runtime_types[0]
        content = create_runtime_content_filed(bitvector, content, input_parameter_types, input_parameter_values)

        variable_values_before_return: dict = runtime_values[1]
        variable_types_before_return: dict = runtime_types[1]
        if len(variable_values_before_return) > 0:
            content = content + f"#### Runtime {place_holder} of variables right before the buggy function's return\n"

            content = create_runtime_content_filed(bitvector, content, variable_types_before_return, variable_values_before_return)
    
    return content


def create_runtime_content_filed(bitvector, content, variable_types_before_return, variable_values_before_return):
    for variable in variable_values_before_return.keys():
        variable_value = variable_values_before_return[variable]["value"]
        variable_type = variable_types_before_return[variable]
        if variable_values_before_return[variable]["omitted"]:
            variable_shape = f", shape: `{variable_values_before_return[variable]['shape']}`"
        else:
            variable_shape = ""

        content = content + f"{variable}, "

        if bitvector["2.2.1"] == 1 and bitvector["2.2.2"] == 1:
            content = content + f"value: `{variable_value}`{variable_shape}, type: `{variable_type}`"
        elif bitvector["2.2.1"] == 1:
            content = content + f"value: `{variable_value}`{variable_shape}"
        elif bitvector["2.2.2"] == 1:
            content = content + f"type: `{variable_type}`"

        content = content + "\n\n"
    return content
