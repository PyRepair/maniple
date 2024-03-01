## Bug Analysis
The buggy function is checking if the second element of the split command.script is equal to 'stash' and if 'usage:' is in the command's stderr. The bug occurs when the command.script is just 'git', which leads to the IndexError because there is only the first element after splitting.

## Bug Fixing Strategy
We need to modify the buggy function to handle the case when the script is only 'git'. We can add a condition to check if the length of the split script is greater than 1 to avoid the IndexError.

## The corrected version of the function
```python
@git_support
def match(command):
    splited_script = command.script.split()
    return (len(splited_script) > 1 and splited_script[1] == 'stash'
            and 'usage:' in command.stderr)
``` 

By checking the length of the splited_script before trying to access the second element, we prevent the IndexError.