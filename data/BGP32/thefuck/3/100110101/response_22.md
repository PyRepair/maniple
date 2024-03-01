### Analysis
In the `info` function, the command to retrieve the Fish shell version is incorrect and does not match the expected output format which causes the test to fail. The error message also shows that the expected result contains only the version number without any additional text.

### Bug
The bug in the `info` function lies in the command used to get the Fish shell version. The command `'echo $FISH_VERSION'` retrieves additional text alongside the version number which causes the assertion error in the test.

### Fix
To fix the bug, we need to update the command to only retrieve the version number without any extra text. We should change the command to `'fish', '--version'` instead of `'fish', '-c', 'echo $FISH_VERSION'`.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```