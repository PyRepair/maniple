### Analysis
The buggy function `info` is supposed to return the version of the Fish shell by running `fish -c 'echo $FISH_VERSION'` command. However, the test is failing because the expected output is `'Fish Shell 3.5.9'`, while the actual output includes the string `'fish, version'`.

### Error
The error is caused by the incorrect formatting of the version string extracted from the command output. The function should only return the version number without the extra text.

### Fix
To fix the bug, we need to modify the code to extract only the version number from the output.

### The corrected version
```python
# The corrected version of the buggy function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]
        return u'Fish Shell {}'.format(version)
```