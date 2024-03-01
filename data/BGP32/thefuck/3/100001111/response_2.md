### Identify the Bug
The bug in the `info` function stems from the fact that it includes the entire string `Fish Shell` in the return string instead of just the version number extracted from the command output.

### Examine the Cause
The function is currently returning `Fish Shell {version}` instead of just `{version}` which is causing issues in certain scenarios such as when using the Oh-My-Fish plugin. This behavior triggers a recursive loop due to the incorrect return format.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the return statement to include only the version number extracted from the command output, rather than prefixing it with "Fish Shell".

### Corrected Version of the Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return version
``` 

By making this change, the `info` function will now correctly return just the version number without any additional text. This corrected version should resolve the issue faced with the Oh-My-Fish plugin and prevent the recursive loop from occurring.