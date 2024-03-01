### Analysis
The function is trying to retrieve the version of the Fish shell by executing a command. However, the way it is handling the output of the command using `proc.stdout.read().decode('utf-8')` seems to be causing the issue. The variable `version` is being set to a string that includes the command itself (`fish, version 3.5.9`) instead of just the version number (`3.5.9`).

### Bug cause
The `proc.stdout.read().decode('utf-8').strip()` is not correctly extracting just the version number from the command output.

### Fix
To fix this issue, we need to make sure that only the version number is extracted from the output of the command. One way to do this is to split the output based on spaces and take the last part, assuming the version number is the last element in the output.

### Corrected version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
``` 

This fix will extract just the version number from the output of the command and return it as expected.