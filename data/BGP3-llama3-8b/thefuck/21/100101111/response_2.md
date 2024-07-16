I will help you fix the bug in the `match` function. The bug is due to incorrect indexing when splitting the `command.script`. When the script is just `git`, `command.script.split()` returns `['git']`, and when you try to access the second element with `[1]`, you get an `IndexError` because the list only has one element.

Here is the corrected version of the `match` function:

```python
@git_support
def match(command):
    return (command.script.split()[0].strip().lower() == 'git' and 'usage:' in command.stderr)
```

In this corrected version, I changed `command.script.split()[1]` to `command.script.split()[0].strip().lower()` to correctly check if the script is just `git`. I also added `.strip().lower()` to make the comparison case-insensitive.

With this corrected function, the test `test_not_match()` should pass, and the GitHub issue should be resolved.