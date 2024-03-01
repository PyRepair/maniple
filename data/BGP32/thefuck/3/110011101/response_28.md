### Analysis
1. The function `info` in the `Fish` class is supposed to retrieve the version of the Fish shell by executing a command `fish -c 'echo $FISH_VERSION'`.
2. The error message indicates that the output of the command is not being processed correctly, resulting in the incorrect version string being returned.
3. The provided runtime values show that the `version` variable contains the entire output of the command, including the initial "fish, version" text.
4. The expected values show that the `version` variable should only contain the version number without the additional text.
   
### Bug
The bug lies in how the output of the command is being processed. The function is returning the entire output of the command as the version string instead of extracting just the version number.

### Fix
To fix the bug, the function should process the command output to extract only the version number. One way to achieve this is by splitting the output based on the comma and extracting the second part, which contains the version number.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        
        # Extracting the version number from the output
        version = output.split(',')[1].strip()
        
        return u'Fish Shell {}'.format(version)
``` 

By extracting the version number correctly and returning it in the desired format, the corrected version of the function should now pass the failing test and return the expected version string 'Fish Shell 3.5.9'.