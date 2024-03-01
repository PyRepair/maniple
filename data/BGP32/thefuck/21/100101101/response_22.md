## Bug analysis
The buggy function `match` is checking if the second word in the command script is 'stash' and if the word 'usage:' is in the command's stderr. The issue here is that the function is splitting the script by whitespaces without considering multiple whitespaces between words.

## Bug fix strategy
To fix this bug, we need to split the script by any whitespace characters (e.g., space, tab, newline) and then check if the second element is 'stash'.

## The corrected version of the function
```python
@git_support
def match(command):
    splited_script = command.script.split()
    return (len(splited_script) > 1
            and splited_script[1] == 'stash'
            and 'usage:' in command.stderr)
``` 

With this correction, the function will split the script correctly and compare the second element to 'stash', fixing the bug.