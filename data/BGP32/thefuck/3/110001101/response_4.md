### Bug Analysis
The bug in the provided function `info` lies in the way the version string extracted from the command output is processed. The current implementation returns the entire output of the command, including the prefix "Fish Shell", which leads to a mismatch with the expected value.

### Bug Explanation
1. In the runtime values for `version`, the value is `'fish, version 3.5.9'`. The expected value should only be `'3.5.9'`.
2. The `u'Fish Shell {}'.format(version)` concatenation includes the string `'Fish Shell'` which leads to the incorrect expected value.

### Fix Strategy
To fix the bug, we need to modify the way the version string is processed. We should extract only the version number from the command output without any prefixes. Then, we can append the extracted version to the string `'Fish Shell'`.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
``` 

With this corrected version, the function will extract only the version number from the output of the command, ensuring that the expected output matches the actual extracted version.