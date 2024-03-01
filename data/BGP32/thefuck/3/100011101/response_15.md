### Analysis
- The current implementation of the `info` function is extracting the shell version from the output of the `fish -c 'echo $FISH_VERSION'` command.
- The expected version is '3.5.9', but the actual extracted version includes the prefix 'fish, version'.
- The test failure indicates that the expected output is 'Fish Shell 3.5.9', while the actual output includes the unnecessary prefix.

### Bug
The bug lies in the way the version is extracted from the command output. The unnecessary 'fish, version' prefix is not being removed.

### Fix
To fix the bug, we need to modify the code to remove the unwanted prefix before formatting the output.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().replace('fish, version ', '')
    return u'Fish Shell {}'.format(version)
``` 

By adding the `replace('fish, version ', '')` method call after `strip()`, we remove the unwanted prefix and ensure that the extracted version matches the expected value.