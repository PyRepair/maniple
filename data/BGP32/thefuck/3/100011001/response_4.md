### Analyzing the Bug
The error message shows that the `info` method of the `Fish` class is returning `'Fish Shell fish, version 3.5.9'` instead of the expected `'Fish Shell 3.5.9'`. This indicates that the `version` variable is not being correctly extracted from the output of the `fish -c 'echo $FISH_VERSION'` command.

### Bug Location
The issue seems to be with how the `version` variable is being extracted from the output of the command.

### Cause of the Bug
The bug is caused by the fact that the output of the `proc.stdout.read()` command is not correctly decoded and stripped, resulting in the additional text `'fish, version'` being included in the `version` variable.

### Strategy for Fixing the Bug
To fix this bug, we need to properly decode and strip the output of the `proc.stdout.read()` command to extract only the version number without any additional text.

### Corrected Version of the Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]
    return u'Fish Shell {}'.format(version)
``` 

By splitting the decoded and stripped output based on `', '` and selecting the second element (index 1), we can extract only the version number without any unwanted text. This corrected version should now pass the failing test.