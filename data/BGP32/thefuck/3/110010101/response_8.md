### Analysis
- The buggy function `info` is supposed to return the name and version of the current shell by executing a command in the Fish shell.
- The error message indicates that the expected output value is `'Fish Shell 3.5.9'` but the actual value is `'Fish Shell fish, version 3.5.9'`.
- The cause of the bug seems to be parsing the output of the command incorrectly, resulting in the unwanted additional text `'fish, version'`.
- To fix the bug, we need to correctly parse the output of the command to extract only the version number without any additional text.

### Fixes
1. Update the logic of extracting the version number from the command output.
2. Remove any unnecessary text before or after the version number.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split(',')[1].strip()
        return u'Fish Shell {}'.format(version)
``` 

This corrected version updates the way the version number is extracted by splitting the output at commas and selecting the second part (assumed to be the version number). It should now return the correct output without extra text.