### Analysis:
The buggy function is supposed to retrieve the version of the Fish shell but is currently not correctly parsing the version information due to the incorrect command and formatting used inside the `Popen` call. The failing test is indicating that the expected version is `'3.5.9'`, while the actual output includes additional text `'fish, version'`.

### Bug:
The bug lies in the command being passed to `Popen` (`'echo $FISH_VERSION'`) which is not retrieving the version information in the desired format. This leads to the extra text being included in the version string causing the assertion to fail.

### Fix:
To fix the bug, we need to modify the command passed to `Popen` to `'fish', '--version'`, which will output just the version number without any additional text.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split()[-1]  # Extracting only the version number
    return u'Fish Shell {}'.format(version)
```