To fix the bug in the provided function, we need to correct the condition that checks for the presence of the word 'stash' in the command script and the word 'usage:' in the command's stderr.

The current condition `command.script.split()[1] == 'stash'` is incorrect because it assumes that the second word in the command script will always be 'stash'. Instead, we should check if 'stash' is in the command script.

Additionally, the condition `and 'usage:' in command.stderr` should be corrected to check if the word 'usage:' is in the command.stderr.

Here is the corrected version of the function:

```python
@git_support
def match(command):
    splited_script = command.script.split()
    return ('stash' in splited_script
            and 'usage:' in command.stderr)
```

This correction ensures that the function checks if 'stash' is present in the command script and if 'usage:' is present in the command's stderr.