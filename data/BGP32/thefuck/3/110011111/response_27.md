## Correction

### Identified Bug:
The issue arises from the way the function handles the output of the command `echo $FISH_VERSION`. It includes unnecessary text along with the version number, causing the comparison in the test to fail.

### Correction Strategy:
To address the bug, we need to extract only the version number from the output of the command `echo $FISH_VERSION` and return it in the correct format.

### Corrected Version

```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
        return u'Fish Shell {}'.format(version)
```

By splitting the output based on `', version '`, we extract only the version number without the unnecessary text. This corrected version will return the version number only, allowing the test to pass successfully.