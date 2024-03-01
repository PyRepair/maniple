### Analysis:
The buggy function `info` in the `Fish` class is supposed to return the version of the Fish shell. The failing test provides the expected output ('Fish Shell 3.5.9') which indicates that the correct version of the Fish shell should be extracted from the command `echo $FISH_VERSION`.

However, the current implementation in the buggy function reads the output of the command without considering the 'fish, version' text which causes a mismatch between the expected and actual version strings. 

The `Popen` call in the buggy function specifies the command `['fish', '-c', 'echo $FISH_VERSION']` but the expected command is actually `['fish', '--version']` as indicated in the failing test.

### Bug:
The bug in the current implementation is due to reading the output of the command directly without considering the contents of the output. Additionally, the command used in `Popen` is incorrect.

### Fix:
1. Change the command in the `Popen` call to `['fish', '--version']` to get the correct version info.
2. Remove the unnecessary text 'fish, version' from the extracted version to match the expected format.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[2]
        return u'Fish Shell {}'.format(version)
``` 

After making these changes, the corrected version of the `info` function should now match the expected output and resolve the bug.