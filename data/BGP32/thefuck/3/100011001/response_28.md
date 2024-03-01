### Explanation:
The bug in the function is related to how the version information is extracted from the output of the `fish -c 'echo $FISH_VERSION'` command. The `version` variable is storing the output as `'fish, version 3.5.9'` instead of just `'3.5.9'`. This causes the assertion to fail because the expected result is `'Fish Shell 3.5.9'`.

### Bug Fix Strategy:
To fix the bug, we need to extract only the version number from the output string. We can do this by splitting the output string and taking the last part, which represents the version number.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]
    return u'Fish Shell {}'.format(version)
```