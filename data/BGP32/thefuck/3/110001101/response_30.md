### Analysis
The buggy function `info` is trying to retrieve the version of the Fish shell by running a command in the terminal. The issue seems to be with the format of the output. The expected version does not match the actual version due to the additional text included in the output.

### Bug Cause
The bug is caused by the extra text "Fish Shell" being added to the version number retrieved from the command output. This causes a mismatch between the expected and actual values.

### Fix Strategy
To fix the bug, we need to modify the code to extract only the version number from the output without any additional text.

### Corrected Version
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return version
```