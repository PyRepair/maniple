### Analysis
1. The `info` function in the `Fish` class is supposed to retrieve the version of the Fish shell. The current implementation is trying to use the `echo $FISH_VERSION` command, but the response format is unexpected.
2. The failing test is setting the expected output as `'Fish Shell 3.5.9'`, indicating that the extracted version should only be the version number.
3. The error message during the failing test asserts an unexpected string format for the version.
4. To fix the bug, the function should extract only the version number from the response of the `echo $FISH_VERSION` command and format it appropriately.

### Bug Cause
The bug is caused by the incorrect parsing of the response from the `echo $FISH_VERSION` command. The current implementation includes unwanted text along with the version number, leading to a mismatch in the expected and actual output.

### Bug Fix
To fix the bug, we need to modify the parsing logic to extract only the version number from the response and format it correctly.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

By splitting the response on the comma and extracting the second part, which should represent the version number, we can ensure that only the version number is considered in the output. This corrected version should pass the failing test and produce the expected output.