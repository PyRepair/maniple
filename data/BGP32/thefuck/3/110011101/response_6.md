### Bug Analysis:
The bug in the `info` function arises from the fact that the variable `version` is being assigned the entire output string from the command `echo $FISH_VERSION`, including the text `fish, version`. This causes a mismatch when comparing the expected output `'Fish Shell 3.5.9'` with `'Fish Shell fish, version 3.5.9'`.

### Bug Fixing Strategy:
To fix this bug, we need to extract only the version number from the output string and then format the return string accordingly.

### Corrected Version:
```python
# The relative path of the file: thefuck/shells/fish.py

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()[13:]  # Extracting only the version number
        return u'Fish Shell {}'.format(version)
``` 

By modifying the `version` assignment to `proc.stdout.read().decode('utf-8').strip()[13:]`, we extract only the version number from the output string, resolving the bug.