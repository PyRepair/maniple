### Analysis
- The buggy function `info` tries to retrieve the version of the Fish shell by running the command `echo $FISH_VERSION` using the `Popen` function.
- The output of the command is not being read correctly, leading to an incorrect version string.
- The test case expects the version string to be `'3.5.9'` but the actual output is `'fish, version 3.5.9'`.

### Bug
The bug lies in how the output of the command executed by `Popen` is being read and processed. The incorrect output format is causing the discrepancy between the expected and actual version string.

### Fix
We need to modify how the output of the `Popen` command is read to extract only the version number without any additional text.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_bytes = proc.stdout.readline()
    version_str = version_bytes.decode('utf-8').strip()
    version = version_str.split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```