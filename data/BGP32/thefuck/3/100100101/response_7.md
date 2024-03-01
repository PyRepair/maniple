### Explanation:
The buggy function `info` is attempting to retrieve the version of the Fish shell by running the command `echo $FISH_VERSION` in a subprocess. However, the test is expecting the version to be retrieved by `fish --version`, instead of `echo $FISH_VERSION`. This mismatch in the command being executed causes the test to fail.

### Bug Fix Strategy:
To fix this bug, we need to update the command being executed in the subprocess to `fish --version` instead of `echo $FISH_VERSION`.

### The corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By making this change, the function will now correctly return the version of the Fish shell and pass the failing test case.