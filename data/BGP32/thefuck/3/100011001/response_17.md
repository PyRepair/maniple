### Analysis:
The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the function is returning `'Fish Shell fish, version 3.5.9'`. This suggests that the function is not correctly parsing the version information from the command output.

The input `'fish, version 3.5.9'` is being read as the version, including the "fish, version" prefix, which is causing the mismatch with the expected output.

### Bug:
The bug is in the line where the version is extracted from the command output:
```python
version = proc.stdout.read().decode('utf-8').strip()
```
This line is not correctly handling the extraction of just the version number without the extra prefix.

### Fix:
To fix this bug, we need to extract only the version number from the output without the extra prefix. We can modify the code to split the output by space and obtain the last element as the version number.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split()[-1]
    return u'Fish Shell {}'.format(version)
```