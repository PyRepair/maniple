### Analysis
1. The buggy function `info` in the `fish.py` file is attempting to retrieve the version of Fish shell by running a command through a subprocess. The test function `test_info` in `test_fish.py` sets the expected version as `3.5.9` but the actual output includes extra information before the version number.
2. The error message shows an assertion error due to the mismatch between the expected output and the actual output.
3. The cause of the bug is that the function `info` is not handling the command output correctly, resulting in additional text retrieved from the command execution that is not part of the version number. The expected output is only the version number.
4. To fix the bug, we need to correctly read and extract only the version number from the command output.

### Bug Fix Strategy
- Modify the function to read the command output correctly and extract only the version number by splitting the output based on the delimiter `','` and then extracting the version number.
- Update the test case to match the expected output of only the version number.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].strip()  # Extracting only the version number
    return u'Fish Shell {}'.format(version)
```

By updating the `info` function as shown above, it correctly extracts the version number from the command output. This should resolve the issue and pass the failing test.