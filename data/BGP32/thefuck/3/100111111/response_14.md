### Bug Explanation
The bug is caused by the incorrect parsing of the `FISH_VERSION` in the `fish` shell within the `info()` function. The `Popen` function is calling `fish -c 'echo $FISH_VERSION'` to get the version string, but the actual output includes more than just the version number, leading to a mismatch in the assertion. This results in an assertion error during the test execution.

To fix this bug, we need to correctly extract the version number from the output of the `Popen` call.

### Bug Fix
Here is the corrected version of the `info()` function that properly extracts the version number:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(" ")[2]
    return u'Fish Shell {}'.format(version)
```

By changing the command to `['fish', '--version']`, we get the full version information of the Fish shell. Then, by splitting the version output by spaces and taking the third element (index 2), we correctly extract the version number only.

This corrected version of the function should resolve the assertion error in the failing test and align with the expected output values.