# Prompt

You need to fix a bug in a python code snippet,  which failed on test when input variable param is None whereas it should return empty list. You need to provide a drop-in replacement, which means minimum changes to source code to pass failed test while won't affect other passed tests. And the fixed patch can be directly used in original project.
The buggy source code is following:

    def cli_bool_option(params, command_option, param, true_value='true', false_value='false', separator=None):
        param = params.get(param)
        assert isinstance(param, bool)
        if separator:
            return [command_option + separator + (true_value if param else false_value)]
        return [command_option, true_value if param else false_value]

# LLM Answer

To fix the bug and handle the case where the param is None while ensuring minimal changes to the source code, you can make the following adjustment:

    def cli_bool_option(params, command_option, param, true_value='true', false_value='false', separator=None):
        param = params.get(param)
        if param is None:
            return []  # Return an empty list when param is None
        assert isinstance(param, bool)
        if separator:
            return [command_option + separator + (true_value if param else false_value)]
        return [command_option, true_value if param else false_value]

I've added a check for param is None at the beginning of the function and returned an empty list in that case. This change ensures that when the input variable param is None, the function will return an empty list as required.

# Fix commit link

https://github.com/ytdl-org/youtube-dl/commit/5b232f46dcbdc805507c02edd4fd598f31d544d5