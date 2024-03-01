## Analysis
1. The `info` function is attempting to get the version of the Fish shell by running the command `fish -c 'echo $FISH_VERSION'` and then extracting the version from the output.
2. The test function `test_info` sets the expected output to `'Fish Shell 3.5.9'` and checks if the command `['fish', '--version']` is called with the `Popen` function.
3. The bug lies in the fact that the command being run in the `Popen` call is `'echo $FISH_VERSION'` instead of `'fish --version'` which results in an incorrect version being extracted.
4. To fix the bug, the command needs to be changed to `'fish --version'` to get the correct version of the Fish shell.

## Fix
```python
# The corrected version of the function
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

In this corrected version, the command passed to `Popen` is changed to `['fish', '--version']` to correctly get the version of the Fish shell. This change will ensure that the function returns the expected output of `'Fish Shell 3.5.9'`.