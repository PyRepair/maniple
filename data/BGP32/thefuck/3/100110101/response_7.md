### Analysis
The buggy function `info` is supposed to return the version of the Fish shell installed by executing a command. The test case provided is mocking the output of the command to `b'fish, version 3.5.9\n'`, but the current implementation of the function is not correctly extracting just the version number. The function is expected to return `'Fish Shell 3.5.9'`, but the actual output contains additional text.

### Bug
The bug lies in how the function processes the output of the command to extract the version number. The function currently just reads the output and uses it as is, without filtering out unnecessary text.

### Fix
To fix the bug, we need to modify the function to extract only the version number from the output of the command. We can achieve this by splitting the output on `,` and then further extracting the version number.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split(',')[1].strip().split()[1]
    return u'Fish Shell {}'.format(version)
```

With this corrected version, the function should now correctly extract the version number from the output and return `'Fish Shell 3.5.9'`.