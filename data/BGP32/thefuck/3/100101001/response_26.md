### Analysis
The `info` function is supposed to retrieve the version of the Fish shell by executing the command `echo $FISH_VERSION` and extracting the output. However, the test is failing because the provided output `b'fish, version 3.5.9\n'` does not match the expected output format of `'3.5.9'`.

### Bug
The bug lies in the inconsistency between the actual output format obtained from the command execution (`fish, version 3.5.9`) and the expected output format (`3.5.9`).

### Fix
To fix this bug, we need to modify the `info` function to correctly extract the version number from the command output. We can achieve this by splitting the output string and extracting the version number part.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].split(' ')[1]
    return u'Fish Shell {}'.format(version)
``` 

By splitting the output string using commas and spaces, we can extract the version number correctly.