The bug in the `info()` function stems from the fact that the command being executed to retrieve the Fish Shell version is incorrect. Instead of using `echo $FISH_VERSION`, the correct command should be `fish --version` to properly fetch the version information.

### Strategy for fixing the bug:
1. Update the command being executed by Popen to `['fish', '--version']` to fetch the Fish Shell version correctly.
2. Adjust the decoding and stripping of the version output accordingly.

### The corrected version of the function:

```python
# The corrected version of the buggy function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split()[-1]  # Extract just the version number
    return f'Fish Shell {version}'
```

By making this correction, the `info()` function will now execute the correct command to obtain the Fish Shell version, extract the version number, and return the expected result. This correction addresses the issue mentioned in the GitHub problem and ensures compatibility with the failing test case.