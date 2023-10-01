def cli_bool_option(params, command_option, param, true_value='true', false_value='false', separator=None):
    param_value = params.get(param)
    assert isinstance(param_value, bool)
    if separator:
        return [command_option + separator + (true_value if param_value else false_value)]
    return [command_option, true_value if param_value else false_value]