The bug in the provided function is that it is not correctly extracting the version information from the output of the 'echo $FISH_VERSION' command. The function is returning the full string "Fish Shell {version}" instead of just the version number.

### Cause of the Bug:
The bug is caused by not properly processing the output from the 'echo $FISH_VERSION' command. The function expects the output to be in the format "fish, version x.y.z" but it should only extract the version number "x.y.z".

### Fix Strategy:
To fix the bug, we need to modify the parsing logic to extract only the version number from the output of the command.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return version
``` 

The corrected version of the function will properly extract just the version number from the output of the command and return it. This will fulfill the expected output values for the test cases.