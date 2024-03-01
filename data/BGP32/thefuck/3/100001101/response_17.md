The bug in the provided function `info` lies in the way the version string is extracted from the command output. The function is currently returning the entire string "fish, version 3.5.9" instead of just the version number "3.5.9".

To fix this bug, we need to modify the code to extract only the version number from the output of the `echo $FISH_VERSION` command.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    
    # Extract only the version number
    version = version.split()[-1]
    
    return u'Fish Shell {}'.format(version)
```

This corrected version will now correctly extract and return only the version number from the output of the `echo $FISH_VERSION` command.