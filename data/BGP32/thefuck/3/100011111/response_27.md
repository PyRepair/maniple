### Analysis
The buggy function `info` in the `fish.py` file is attempting to obtain the version of the Fish shell by running the command `fish -c 'echo $FISH_VERSION'`. However, the output of the command is not being parsed correctly, resulting in the version string being `fish, version 3.5.9` instead of just `3.5.9`. This mismatch leads to the failing test assertion due to the unexpected format of the version string.

### Error Cause
- The error occurs because the function is not stripping the unnecessary text (`fish, version`) from the version output.
- The failure happens as the expected version format in the tests is not matching the actual version format retrieved in the function.

### Fix Strategy
To fix the bug, we need to modify the code to only extract the version number from the output and format it properly before returning the final string.

### The Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version_number = version.split(',')[1].strip()
    return u'Fish Shell {}'.format(version_number)
``` 

With this corrected version, the function will properly extract the version number from the output, regardless of any additional text present, and return the expected format like `Fish Shell 3.5.9`.