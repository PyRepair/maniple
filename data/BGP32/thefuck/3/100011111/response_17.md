### Analysis
The buggy function `info` is attempting to retrieve the version of the Fish shell by executing a command using `Popen`, but it is not correctly parsing the output. The error message highlights that the expected output is `'Fish Shell 3.5.9'` but the actual output includes the string `'fish, version 3.5.9'`.

The root cause of the bug is that the return value of `echo $FISH_VERSION` includes additional text that is not needed for the version number, hence causing the incorrect comparison in the test.

### Fix Strategy
To fix this bug, we need to modify the parsing of the output from the command execution to extract only the version number without any additional text.

### The corrected version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    
    # Extract only the version number
    version = version.split(',')[1].strip()
    
    return u'Fish Shell {}'.format(version)
```

By splitting the `version` string using `','`, we can isolate and strip the version number without the extra text. This corrected version should now accurately return the version number without additional text, resolving the failing test case.