The bug in the current function is that it checks if the second element of the split command script is 'stash', but it should actually check the first element. This is because the command.script should be 'git' and not 'stash'.

To fix this bug, we need to change the comparison index from [1] to [0] to compare the first element of the split command script.

Here is the corrected version of the function:

```python
@git_support
def match(command):
    splited_script = command.script.split()
    return (splited_script[0] == 'git'
            and 'usage:' in command.stderr)
``` 

This way, the function will correctly check if the first element of the split command script is 'git' and if the 'usage:' string is in the command's stderr, as expected.