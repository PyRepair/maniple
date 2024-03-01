### Analysis
The issue in the `info` function seems to be related to the way the subprocess output is read and decoded. The `Popen` function is used to run a command to get the `FISH_VERSION`, but the reading and decoding of the output are not done correctly, which leads to the incorrect `version` value being returned.

### Bug Explanation
1. The `proc.stdout.read()` function returns a `MagicMock` object instead of the actual output string.
2. The process' standard output needs to be read first before decoding it into a string to get the `version`.

### Fix
We need to correctly read the output of the subprocess before decoding it to get the `version` value.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output, _ = proc.communicate()
    version = output.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
``` 

In the corrected version, we use the `proc.communicate()` method to read the output of the subprocess and then decode it to get the `version` value. This should fix the bug and return the correct version of the Fish shell.