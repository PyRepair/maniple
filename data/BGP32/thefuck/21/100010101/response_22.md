### Explanation
The bug in the `match` function arises from the assumption that the `command.script` attribute will always contain multiple words separated by spaces. When the script is just "git" without any additional arguments, accessing the index 1 of `split()` method will cause an `IndexError`.

### Bug Fix Strategy
To fix this bug, we need to check if the split command has enough words before accessing the index 1.

### The corrected version of the function
```python
@git_support
def match(command):
    splited_script = command.script.split()
    return (len(splited_script) > 1
            and splited_script[1] == 'stash'
            and 'usage:' in command.stderr)
``` 

This corrected version first splits the command script and then checks if there are more than one word before accessing index 1.