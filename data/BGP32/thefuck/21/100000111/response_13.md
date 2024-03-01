## Analysis
The `match` function is designed to check if the second word in the `command.script` is `'stash'` and if the `command.stderr` contains the string `'usage:'`. However, in the provided cases, the `command.script` is just `'git'` which leads to an `IndexError` because there is no second word to split.

## Bug Explanation
The bug occurs because the function assumes there will always be a second word in the `command.script` to compare with `'stash'`. It doesn't handle the edge case where the script is just `'git'`.

## Bug Fix
We need to add a check to verify that there are enough words in the `command.script` before attempting to access the second word. If there are not enough words, we can return `False`.

## Updated Function
```python
@git_support
def match(command):
    splited_script = command.script.split()
    return (len(splited_script) > 1
            and splited_script[1] == 'stash'
            and 'usage:' in command.stderr)
```

With this updated function, we first split the command script into words and then check if there are enough words before comparing the second word with `'stash'`. This modification should prevent the `IndexError` and handle the edge case where the script is just `'git'`.