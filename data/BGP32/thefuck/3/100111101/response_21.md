### Analysis:
1. The buggy function `info` is supposed to return the version of the Fish shell by executing a command `echo $FISH_VERSION` using the `Popen` function.
2. The failing test is checking if the returned version matches the expected output `'Fish Shell 3.5.9'`.
3. The error occurs because the actual output includes additional text `fish,` which is not expected.
4. The bug is likely caused by the command used (`echo $FISH_VERSION`) returning unexpected output format which includes `fish,` before the version number.
5. To fix the bug, we need to modify the command to extract only the version number without any additional text.

### Bug Fix:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'fish --version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(', version ')[1]  # Extract version number
    return u'Fish Shell {}'.format(version)
```

With this fix, the command used to retrieve the version number is modified to `fish --version`, and then we extract only the version number part from the returned output. This change ensures that the returned version matches the expected format `'Fish Shell X.X.X'`.