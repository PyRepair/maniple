The buggy function `info` in the `fish.py` file is incorrectly fetching the version of the Fish shell. The issue lies in the command used to get the version (`$FISH_VERSION`) and how it is parsed from the output.

### Bug Cause:
- The buggy function is using the command `'echo $FISH_VERSION'` to get the Fish shell version, but the shell command to get the Fish version should be `'fish --version'`.
- The function is expecting the version to be just a number (e.g., `'3.5.9'`), but it is actually getting the output `'fish, version 3.5.9'` which leads to the assertion error in the test.

### Fix Strategy:
- Update the command in the `Popen` call to `'fish --version'` to correctly fetch the Fish shell version.
- Parse the output to extract only the version number (e.g., `'3.5.9'`).

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(',')[1].strip().split()[1]
    return u'Fish Shell {}'.format(version)
```

This corrected version will correctly fetch the Fish shell version using `'fish --version'`, extract the version number, and return it in the expected format.