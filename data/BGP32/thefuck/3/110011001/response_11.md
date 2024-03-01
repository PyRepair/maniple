### Analysis
- The buggy function attempts to retrieve the Fish shell version by executing a command, but the output includes additional text "fish, version" that is not needed in the final version string.
- The error message indicates the discrepancy between the expected output ('Fish Shell 3.5.9') and the actual output ('Fish Shell fish, version 3.5.9').

### Bug Cause
The bug is caused by not parsing the output of the command correctly to extract only the version number without the extra text.

### Fix Strategy
To fix the bug, we need to modify the function to extract only the version number from the output string.

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
        
        # Extract only the version number without the extra text
        version_number = version.split(',')[1].strip()
        
        return u'Fish Shell {}'.format(version_number)
```