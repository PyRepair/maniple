### Analysis:
- The `info` function in the `fish.py` file is supposed to return the name and version of the current Fish shell by running `echo $FISH_VERSION` command.
- The failing test is trying to assert that the returned value from `info` function is 'Fish Shell 3.5.9'.
- The error message indicates that the comparison fails due to an unexpected format in the returned value.
- The test case mocks the `Popen` function to return `b'fish, version 3.5.9\n'` which is the format the function expects.
- The buggy function might be incorrectly extracting the version information.

### Error:
The bug in the `info` function occurs because the expected output format '3.5.9' is not matching with the actual output format 'fish, version 3.5.9'.

### Fix Strategy:
Modify the logic of extracting the version string from the output of the `echo $FISH_VERSION` command to match the expected format.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split(' ')[-1]
    return f'Fish Shell {version}'
```

By splitting the `version_output` on spaces and selecting the last element, we can extract just the version number. This modification will ensure that the returned version format matches the expected value '3.5.9' in the failing test case.