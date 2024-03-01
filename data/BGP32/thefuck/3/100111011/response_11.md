### Error Analysis:
- The `info` function in `fish.py` is trying to fetch the Fish Shell version using the command `echo $FISH_VERSION`, but the test is expecting the version with the command `fish --version`. This discrepancy causes the test failure.
- The error message clearly indicates that the actual output `'Fish Shell fish, version 3.5.9'` is different from the expected output `'Fish Shell 3.5.9'`.
- The GitHub issue mentions that the plugin is triggering a recursive loop due to this discrepancy.

### Fix Strategy:
To fix the bug, we need to modify the command used to fetch the Fish Shell version in the `info` function to match the command expected by the test.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]
    return u'Fish Shell {}'.format(version)
```

After making this correction in the `fish.py` file, running the failing test should pass successfully without any assertion errors.