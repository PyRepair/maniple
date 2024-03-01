The bug in the provided function `info` is caused by the incorrect output formatting of the Fish Shell version. The function currently returns the version as `'fish, version X.X.X'` instead of just `'X.X.X'`. This incorrect format causes issues with other components that use the version information.

To fix this bug, we need to modify the code to extract and return only the actual version number without any additional text.
Below is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split()[2]  # Extract only the version number
    return u'Fish Shell {}'.format(version)
```

By splitting the version string and extracting only the version number portion, the function now correctly outputs just the version number without any additional text. This correction adheres to the expected output values and resolves the issue mentioned in the GitHub bug report related to the incorrect output formatting of the Fish Shell version.