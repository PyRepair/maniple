### Bug Explanation

The bug in the `info` function of the `Fish` class is due to the incorrect command being used to retrieve the Fish shell version. The command 'echo $FISH_VERSION' does not return a simple version number like '3.5.9', but rather includes extra information such as 'fish, version 3.5.9'.

This discrepancy causes the assertion in the test function to fail because the expected version format is 'Fish Shell 3.5.9' but the actual format is 'Fish Shell fish, version 3.5.9'. This bug was reported in a GitHub issue due to its impact on the initialization of the Fish shell with the Oh-My-Fish plugin, causing a recursive loop.

### Fix Strategy

To fix this bug, the command used to retrieve the Fish shell version needs to be changed to extract only the version number without any additional text. This can be achieved by modifying the command executed by Popen to 'fish --version' which directly returns the version information without any other text.

### Corrected Version

```python
# Updated version of the buggy function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

By updating the command to 'fish --version' and then extracting only the version number part, the corrected function should now return the correct format 'Fish Shell 3.5.9' as expected by the test function.