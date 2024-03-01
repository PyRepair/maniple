The buggy function's logic is trying to split the `command.script` by spaces and check if the second element is equal to 'stash'. However, the error occurs because the split operation might result in a list with only one element (if the script does not contain any spaces), causing an IndexError when trying to access the second element.

To fix this bug, we need to first check if the split operation generates at least two elements before comparing the second element with 'stash'.

Here is the corrected version of the function:

```python
@git_support
def match(command):
    splited_script = command.script.split()
    return (len(splited_script) > 1 
            and splited_script[1] == 'stash'
            and 'usage:' in command.stderr)
``` 

This correction ensures that the script is split regardless of the number of spaces in it, preventing the IndexError.