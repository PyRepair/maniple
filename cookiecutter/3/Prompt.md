You need to fix a bug in a python code snippet.

The buggy source code with comment inside is following, and you should follow all specification in comment:

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
        prompt = u'\n'.join((
            u'Select {}:'.format(var_name),
            u'\n'.join(choice_lines),
            u'Choose from {}'.format(u', '.join(choices))
        ))

        user_choice = click.prompt(
            prompt, type=click.Choice(choices), default=default
        )
        return choice_map[user_choice]


The definition of click API is following:

click.prompt(text, default=None, hide_input=False, confirmation_prompt=False, type=None, value_proc=None, prompt_suffix=': ', show_default=True, err=False)
Prompts a user for input. This is a convenience function that can be used to prompt a user for input later.

If the user aborts the input by sending a interrupt signal, this function will catch it and raise a Abort exception.

New in version 4.0: Added the err parameter.

Parameters
text ¡V the text to show for the prompt.

default ¡V the default value to use if no input happens. If this is not given it will prompt until it¡¦s aborted.

hide_input ¡V if this is set to true then the input value will be hidden.

confirmation_prompt ¡V asks for confirmation for the value.

type ¡V the type to use to check the value against.

value_proc ¡V if this parameter is provided it¡¦s a function that is invoked instead of the type conversion to convert a value.

prompt_suffix ¡V a suffix that should be added to the prompt.

show_default ¡V shows or hides the default value in the prompt.

err ¡V if set to true the file defaults to stderr instead of stdout, the same as with echo.


The raised issue discription is 'Fix typos'.

You need to provide a drop-in replacement, with 'minimum changes to source code' that 'pass failed test' while 'won't affect other already passed tests'. And the fixed patch can be directly used in original project.