### Analysis
The buggy function `info()` is trying to get the version of the Fish shell by running a command and reading the output. However, the output is not being parsed correctly, resulting in the version being extracted as `'fish, version 3.5.9'` instead of just `'3.5.9'` as expected.

The error message shows the actual output being `'fish, version 3.5.9'` instead of `'3.5.9'`, leading to the assertion error.

### Bug Cause
The bug is caused by not properly parsing the output of the command to extract only the version number. The `echo $FISH_VERSION` command includes additional information such as `'fish, version'` in the output, which is not needed.

### Fix Strategy
To fix the bug, we need to modify the code to only extract the version number from the command output. This can be done by splitting the output string and extracting the version part.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        
        # Extract only the version number
        version = version.split(", version ")[1]
        
        return u'Fish Shell {}'.format(version)
``` 

With this correction, the function will correctly extract and return the version number without the extra `'fish, version'` prefix, resolving the failing test case.