Here is the corrected version of the function:

```python
@git_support
def match(command):
    words = command.script.split()
    if len(words) >= 2 and words[1] == 'stash':
        return 'usage:' in command.stderr
    return False
```

Explanation:

* The bug in the original function is that it assumes the `command.script` will always contain at least two elements when split by spaces (`script.split()`). However, if the user simply runs `git` without any arguments, `command.script` will only contain one element (`['git']`). In this case, attempting to access the second element (`words[1]`) will raise an `IndexError`.
* The corrected function first checks if the length of the `words` list is at least 2, and if the second element (`words[1]`) is `'stash'`. If these conditions are met, it checks if `'usage:'` is in `command.stderr`. If not, it returns `False`.
* This corrected function will now correctly match the `git stash` command even when the user runs `git` without any arguments.

This fix ensures that the function handles the use case where the user runs `git` without any arguments and still correctly checks if the command is `stash` and if `'usage:'` is in `command.stderr`.