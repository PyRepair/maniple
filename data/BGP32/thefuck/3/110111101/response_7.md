### Strategy for fixing the bug:
The bug seems to be in the incorrect parsing of the version string obtained from the command output. The function is currently returning the entire string 'fish, version 3.5.9' instead of just the version number '3.5.9'. To fix this bug, we need to modify the way we extract the version number from the output string.

### Corrected version of the function:

```python
# The relative path of the buggy file: thefuck/shells/fish.py

# The declaration of the class containing the buggy function
class Fish(Generic):
    # Corrected version of the buggy function
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
```