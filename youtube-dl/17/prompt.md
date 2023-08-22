You need to fix a bug in a python code snippet, which failed on test when input variable param is None whereas it should return empty list.

The buggy source code is following:

    def cli_bool_option(params, command_option, param, true_value='true', false_value='false', separator=None):
        param = params.get(param)
        assert isinstance(param, bool)
        if separator:
            return [command_option + separator + (true_value if param else false_value)]
        return [command_option, true_value if param else false_value]


And the raised issue description for this bug is 'In CurlFD, this line cmd += self._bool_option('--continue-at', 'continuedl', '-', '0') will fail since continuedl value is None, unless it is explicitly specified in the options'. (don't use this description, it's unclear and misleading)


You need to provide a drop-in replacement, with 'minimum changes to source code' that 'pass failed test' while 'won't affect other already passed tests'. And the fixed patch can be directly used in original project.