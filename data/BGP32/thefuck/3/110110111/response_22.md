To fix the bug in the `info` function of the `Fish` class, we need to address the following issues:

1. The command used to retrieve the Fish shell version is incorrect. Instead of using `'echo $FISH_VERSION'`, it should use `'fish --version'`.
2. The comparison in the test function is failing because the returned value includes additional text ("fish, version") that needs to be removed before formatting.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(', version ')[1]  # Get only the version number
    return u'Fish Shell {}'.format(version)
```

By using `['fish', '--version']` as the command and extracting only the version number from the output, the function should now return the correct version string without additional text.

The corrected function should pass the failing test and satisfy the expected input/output values.