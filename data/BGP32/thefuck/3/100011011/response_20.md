### Analyzing the buggy function and error message
The buggy function `info` is attempting to get the version of the Fish Shell by running a command using Popen and then extracting the version from the output. The error message indicates that the version extracted includes additional text "fish, version" which causes the assertion to fail. The test expects only the version number.

### Error Location
The error is likely in the line that constructs the return string:
```python
return u'Fish Shell {}'.format(version)
```
The `version` variable is not just the version number but also includes the text "fish, version".

### Cause of the Bug
The `version` variable includes more text than just the version number. This extra text "fish, version" is causing the assertion to fail in the test.

### Strategy for Fixing the Bug
To fix the bug, we need to extract only the version number from the `version` variable before constructing the return string.

### Corrected Version of the Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    
    # Extract just the version number
    version = output.split(',')[-1].strip()
    
    return u'Fish Shell {}'.format(version)
``` 

By making this change, we extract only the version number from the output, ensuring that the constructed return string contains only the version number as required by the test.