## Bug Fix
The bug in the provided function is related to the incorrect formatting of the `version` variable. The value retrieved from the command `echo $FISH_VERSION` includes the text "fish, version" before the actual version number. To fix this bug, we need to extract only the version number without the text "fish, version".

### Corrected Version of the Function
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):
    
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split()[-1]  # Extract only the version number
        return u'Fish Shell {}'.format(version)
```

By splitting the `version` string obtained from the command output and selecting the last element, we can extract only the version number without any additional text. This corrected version should now return the expected output and pass the failing test.