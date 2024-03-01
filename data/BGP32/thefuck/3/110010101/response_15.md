### Analysis
1. The buggy function `info` is trying to get the version of the Fish shell by running a subprocess command. The expected output is in the format "Fish Shell \<version>", but the current implementation is not extracting the version correctly.
2. The error message indicates that the output of the subprocess is "fish, version 3.5.9" instead of just the version number.
3. The bug is caused by the incorrect parsing of the output to extract only the version number. Since the actual output includes extra text, the comparison fails.
4. To fix the bug, we need to extract only the version number from the output of the subprocess command before formatting it into the desired string format.

### Solution
I will modify the function to extract only the version number from the output before creating the final string.

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split(", version ")[1]
        return u'Fish Shell {}'.format(version)
``` 

This modification ensures that only the version number is extracted from the output of the subprocess command, which should fix the bug.