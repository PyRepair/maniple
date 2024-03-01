### Analysis
1. The buggy function `info` is attempting to get the version of the Fish shell using the command `echo $FISH_VERSION`. However, the output of this command contains more than just the version number.
2. The error message indicates that the comparison between the actual output (`'Fish Shell fish, version 3.5.9'`) and the expected output (`'Fish Shell 3.5.9'`) fails because the version number is not extracted properly.
3. The actual output includes unnecessary text before the version number ('fish, version') which causes the assertion error. The version number '3.5.9' is not extracted correctly from the output.
4. To fix the bug, we need to modify the code to only extract the version number from the output and format the output string accordingly.

### Fix
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split()[-1]  # Extracting the last element of the split output
        return u'Fish Shell {}'.format(version)
``` 

By splitting the output of the command and extracting the last element (which should be the version number) before formatting it into the output string, the corrected function should now provide the expected output.