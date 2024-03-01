### Bug Explanation:
The bug in the `info` function of the `Fish` class is causing a recursive loop when the `thefuck -v` command is used with the Oh-My-Fish plugin. This is due to the fact that the function is trying to get the Fish Shell version in a way that triggers the regeneration of functions, leading to the infinite loop.

### Bug Fix Strategy:
To fix the bug, we need to modify the way the Fish Shell version is retrieved in the `info` function to avoid triggering the regeneration of functions. One approach could be to directly read the version information without causing side effects that lead to the recursive loop.

### Corrected Version:
Here is the corrected version of the `info` function in the `Fish` class:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').split()[-1]
        return u'Fish Shell {}'.format(version)
```

In this corrected version:
- We are using `Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)` to directly get the Fish Shell version without triggering any side effects.
- We extract the version from the output of the command without causing any functions to be regenerated, avoiding the recursive loop issue mentioned in the GitHub bug report.

This corrected version should resolve the issue reported in the GitHub issue related to the Oh-My-Fish plugin with the thefuck -v command.