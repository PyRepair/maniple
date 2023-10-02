You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

	def cli_bool_option(params, command_option, param, true_value='true', false_value='false', separator=None):
		param = params.get(param)
		assert isinstance(param, bool)
		if separator:
			return [command_option + separator + (true_value if param else false_value)]
		return [command_option, true_value if param else false_value]



The raised issue description for this bug is: 'In CurlFD, this line cmd += self._bool_option('--continue-at', 'continuedl', '-', '0') will fail since continuedl value is None, unless it is explicitly specified in the options'.



You need to provide a drop-in replacement, with 'minimum changes to source code' that 'pass failed test' while 'won't affect other already passed tests'. And the fixed patch can be directly used in original project.