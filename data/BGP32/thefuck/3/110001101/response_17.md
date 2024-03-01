### Analysis
The buggy function `info` is attempting to retrieve the version of the Fish shell by executing a command using `Popen`. However, the bug lies in how the function processes the output of the command. The function is not correctly extracting the version number from the output, resulting in an incorrect return value.

### Bug Cause
The bug is caused by not correctly parsing the output of the command executed. The function is not extracting the version number from the output string properly.

### Fix Strategy
1. Update the function to properly decode and extract the version number from the command output.
2. Since the expected version output only includes the version number without any additional text, we need to modify the function to extract just the version number.

### Corrected Version
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        # Extract only the version number
        version = version.split(", version ")[-1]  
        return u'Fish Shell {}'.format(version)
``` 

By splitting the `version` string at ", version " and taking the last element, we can extract only the version number. This corrected version of the function should now return the expected version number without any additional text.