You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

	def read_user_choice(var_name, options):
		"""Prompt the user to choose from several options for the given variable.

		The first item will be returned if no input happens.

		:param str var_name: Variable as specified in the context
		:param list options: Sequence of options that are available to select from
		:return: Exactly one item of ``options`` that has been chosen by the user
		"""
		# Please see http://click.pocoo.org/4/api/#click.prompt
		if not isinstance(options, list):
			raise TypeError

		if not options:
			raise ValueError

		choice_map = OrderedDict(
			(u'{}'.format(i), value) for i, value in enumerate(options, 1)
		)
		choices = choice_map.keys()
		default = u'1'

		choice_lines = [u'{} - {}'.format(*c) for c in choice_map.items()]
		prompt = u'
'.join((
			u'Select {}:'.format(var_name),
			u'
'.join(choice_lines),
			u'Choose from {}'.format(u', '.join(choices))
		))

		user_choice = click.prompt(
			prompt, type=click.Choice(choices), default=default
		)
		return choice_map[user_choice]



The raised issue description for this bug is: 'Fix typos'.



You need to provide a drop-in replacement, with 'minimum changes to source code' that 'pass failed test' while 'won't affect other already passed tests'. And the fixed patch can be directly used in original project.