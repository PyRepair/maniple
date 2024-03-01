### Identify the Bugs:
1. The `shell.info()` function is not correctly retrieving the `FISH_VERSION`.
2. The assertion in the test is expecting `'Fish Shell 3.5.9'` but the current implementation returns `'Fish Shell fish, version 3.5.9'`.
3. The error message indicates a mismatch in the expected output and the actual output.

### Explain the Cause of the Bug:
The bug lies in the `info()` function of the `Fish` class that is trying to extract the Fish Shell version from the command `echo $FISH_VERSION` but the expected output and method of retrieving the version are incorrect. The failing test `test_info()` expects a specific output format, causing the mismatch error.

### Suggested Strategy for Fixing the Bug:
1. Modify the command to retrieve the Fish Shell version correctly.
2. Ensure that the output format matches the expected output in the failing test.

### Corrected Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[2]
    return u'Fish Shell {}'.format(version)
```

### Changes Made:
1. Changed the command from `'echo $FISH_VERSION'` to `['fish', '--version']`.
2. Modified the way to extract the version from the output to match the expected format.

This corrected version should resolve the issue and pass the failing test.