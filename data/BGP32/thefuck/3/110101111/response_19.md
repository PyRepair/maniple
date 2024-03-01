## Fixing the Bug

### Analysis:
The bug in the `info` function of the `Fish` class is caused by the incorrect command being executed to get the Fish shell version. The test expects the version number to be extracted using `fish --version` but the actual command used is `fish -c 'echo $FISH_VERSION'`. This discrepancy leads to the test failing.

### Strategy for Fixing the Bug:
To fix the bug, we need to update the command used to retrieve the Fish shell version to `fish --version`.

### Corrected Version of the Function:

```python
# The relative path of the buggy file: thefuck/shells/fish.py

# The declaration of the class containing the buggy function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(", version ")[1]
        return u'Fish Shell {}'.format(version)
```

This corrected version of the function will now execute the correct command `fish --version` to retrieve the version of the Fish shell. The function will strip the output to extract only the version number and return it in the expected format.