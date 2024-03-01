### Analysis:
- The error message shows that the `info` function is returning a string with an incorrect format of the version information.
- The expected format of the returned string should be `'Fish Shell 3.5.9'`.
- The value obtained from `proc.stdout.read().decode('utf-8').strip()` is `'fish, version 3.5.9'`.
- The issue seems to be related to how the version information is retrieved and formatted.
- The variable `version` in the buggy function is directly using the output of the command without proper parsing.

### Bug:
The bug in the function is that it is not extracting the version number correctly from the output of the `fish -c 'echo $FISH_VERSION'` command. It is returning the entire output instead of just the version number.

### Fix:
To fix the bug, we need to parse the version number correctly from the output of the command.

### The corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
``` 

With this correction, the function will correctly extract and format the version number from the output of the command, resulting in the expected output `'Fish Shell 3.5.9'`.