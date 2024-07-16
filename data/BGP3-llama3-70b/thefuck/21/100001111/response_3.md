Here is the corrected version of the buggy function:

```python
@git_support
def match(command):
    words = command.script.split()
    return len(words) > 1 and words[1] == 'stash' and 'usage:' in command.stderr
```

Explanation:

The bug occurs because the function assumes that `command.script.split()` will always have at least two elements, which is not the case when the script is just 'git'. 

The fix involves checking if the list of words has at least two elements before trying to access the second element. This prevents the `IndexError: list index out of range` exception.

The GitHub issue description suggests that the `git_fix_stash` rule fails when the script is just 'git', which is consistent with the bug. The corrected function should resolve this issue.