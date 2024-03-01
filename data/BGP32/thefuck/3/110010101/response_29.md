## Analysis
The buggy function `info()` in the `Fish` class is attempting to retrieve the version of the Fish shell by executing a command `fish -c 'echo $FISH_VERSION'`. However, the function is not correctly extracting and formatting the version information from the output.

In the failing test case, the expected version is '3.5.9', but the actual version extracted from the command output includes extra text ('fish, version').

The bug is likely occurring because the function is not properly extracting just the version number from the output of the shell command.

## Bug Fix Strategy
To fix the bug, we need to modify the way the function extracts the version number from the output of the shell command. We should parse the output to extract just the version number without any additional text.

## Code Fix
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version_output = proc.stdout.read().decode('utf-8').strip()
        
        # Extract only the version number from the output
        version = version_output.split(", version ")[1]
        
        return u'Fish Shell {}'.format(version)
``` 

With this fix, the function will correctly extract just the version number from the output of the shell command and return it in the desired format.