The bug in the current function lies in the condition `command.script.split()[1] == 'stash'`. This condition checks if the second word in the command script is 'stash', but in the input command `'git'`, there is no second word which causes the function to throw an index out of range error.

To fix this bug, we need to first check if the script has more than one word before trying to access the second word. We can also update the condition to check if the first word is 'git' and the second word is 'stash'.

Here is the corrected version of the function:

```python
@git_support
def match(command):
    splited_script = command.script.split()
    return (len(splited_script) > 1
            and splited_script[0] == 'git' 
            and splited_script[1] == 'stash'
            and 'usage:' in command.stderr)
``` 

This corrected version will now correctly handle the input conditions and return the desired output values for the provided test case.