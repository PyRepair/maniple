To fix the bug in the `info` function of the `Fish` class, we need to update the command being used to get the Fish Shell version and properly format the version string.

Explanation of the bug:
1. The function is attempting to get the version of Fish Shell using the command `echo $FISH_VERSION`, which is not the correct way to get the version.
2. The test is expecting the version string to be in a specific format ('Fish Shell 3.5.9'), but the function is returning 'Fish Shell fish, version 3.5.9' which is incorrect.

Strategy for fixing the bug:
1. Update the command used to get the Fish Shell version to `fish --version` to correctly retrieve the version.
2. Extract the version number from the output and format it as 'Fish Shell x.x.x'.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].strip().split(' ')[1]  # Extract version number
    return 'Fish Shell {}'.format(version)
```

This corrected version of the function should now correctly retrieve the Fish Shell version and format it as expected by the test. It addresses the issue described in the GitHub report as well.