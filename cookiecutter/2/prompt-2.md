You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

	def find_hook(hook_name, hooks_dir='hooks'):
		"""Return a dict of all hook scripts provided.

		Must be called with the project template as the current working directory.
		Dict's key will be the hook/script's name, without extension, while values
		will be the absolute path to the script. Missing scripts will not be
		included in the returned dict.

		:param hook_name: The hook to find
		:param hooks_dir: The hook directory in the template
		:return: The absolute path to the hook script or None
		"""
		logger.debug('hooks_dir is %s', os.path.abspath(hooks_dir))

		if not os.path.isdir(hooks_dir):
			logger.debug('No hooks/dir in template_dir')
			return None

		scripts = []
		for hook_file in os.listdir(hooks_dir):
			if valid_hook(hook_file, hook_name):
				return os.path.abspath(os.path.join(hooks_dir, hook_file))

		return None



The raised issue description for this bug is: 'Generated projects can use multiple type hooks at same time'.



You need to provide a drop-in replacement, with 'minimum changes to source code' that 'pass failed test' while 'won't affect other already passed tests'. And the fixed patch can be directly used in original project.