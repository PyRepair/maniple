## Analysis
The buggy function `info` is attempting to retrieve the version of the Fish shell using the command `echo $FISH_VERSION`. However, in the failing test, the expected output version is provided in a different format (`fish, version 3.5.9\n`), which is not being handled correctly by the function.

## Bug Explanation
The bug in the function is due to the mismatch between the expected output format and the command used to retrieve the version. The function expects just the version number `3.5.9`, but the test provides it in the format `fish, version 3.5.9\n`.

## Fix
To fix the bug, we need to modify the command used to retrieve the version in the `info` function. We can use the command `fish --version` to capture the version number in the correct expected format. 

Here is the corrected version of the function:

```python
# The relative path of the corrected file: thefuck/shells/fish.py

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
``` 

This corrected version will use the correct command to retrieve the version in the expected format.