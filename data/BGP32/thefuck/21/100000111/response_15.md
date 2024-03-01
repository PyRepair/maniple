The buggy function is checking if the second word in `command.script` is 'stash' and if the 'usage:' string is present in `command.stderr`. However, if the script is just 'git' and there is no second word to check, it will result in an `IndexError` because the split list will be empty.

To fix this issue, we need to first check if the split list has at least two elements before trying to access the second element.

Here is the corrected version of the function:

```python
@git_support
def match(command):
    splited_script = command.script.split()
    return (len(splited_script) >= 2 and splited_script[1] == 'stash'
            and 'usage:' in command.stderr)
``` 

This corrected version first checks if the length of `splited_script` is at least 2 before comparing the second element with 'stash'. This way, the function will not raise an `IndexError` when the script is only 'git'.