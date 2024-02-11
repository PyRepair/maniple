There are a few issues with the get_new_command function:

1. The first pop call is redundant since both the previous if conditions delete the value twice. 

Let's fix the function by removing the redundant pop call and handling the case when '-u' is passed along with the argument.

```python
@git_support
def get_new_command(command):
    # If --set-upstream or -u are passed, remove it and its argument. This is
    # because the remaining arguments are concatenated onto the command suggested
    # by git, which includes --set-upstream and its argument
    try:
        upstream_option_index = command.script_parts.index('--set-upstream')
    except ValueError:
        try:
            upstream_option_index = command.script_parts.index('-u')
        except ValueError:
            upstream_option_index = -1

    if upstream_option_index > -1:
        command.script_parts.pop(upstream_option_index)
        # Check if -u is passed with an argument
        if command.script_parts[upstream_option_index] == '-u':
            command.script_parts.pop(upstream_option_index)    

    push_upstream = command.stderr.split('\n')[-3].strip().partition('git ')[2]
    return replace_argument(" ".join(command.script_parts), 'push', push_upstream)
```

This corrected version of the function should solve the pop index out of range issue and handle the case when '-u' is passed with an argument.

Revised function is provided above with changes highlighted. This should now fix the issue and match the expected behavior.