### Analysis
- The error message indicates that the `info` function is returning the incorrect version string for the Fish shell.
- The expected version string is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`.
- The issue seems to be related to how the version information is extracted from the `proc` variable.

### Bug Cause
The bug in the function is that the version information is extracted directly from the output of the `proc.stdout.read()` method without properly decoding and formatting the output. This results in the version string containing additional unwanted characters.

### Fix Strategy
1. Decode the output of `proc.stdout.read()` using the `utf-8` encoding to get the string representation.
2. Strip any leading/trailing whitespaces from the decoded string.
3. Properly format the extracted version string as `'Fish Shell <version>'`.

### Corrected Version
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The corrected version of the class containing the fixed function
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
        return u'Fish Shell {}'.format(version)
``` 

With the corrected version, the function will properly extract the version string, decode it, remove any leading/trailing whitespaces, and format it as `'Fish Shell <version>'`. This should resolve the bug and make the function return the correct version string.