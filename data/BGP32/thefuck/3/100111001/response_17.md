### Bug Analysis
The failing test is expecting the output of the `info` function to be `'Fish Shell 3.5.9'` but is getting `'Fish Shell fish, version 3.5.9'`. This indicates that there is an issue with how the version information is retrieved and formatted in the `info` function. The error message also suggests that the command used to fetch the version might not be correct.

### Bug Location
The bug is likely located in how the version information is extracted from the output of the command in the `info` function. The line `proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)` is where the command is executed to get the version, and the subsequent manipulation of the output is causing the issue.

### Bug Explanation
The bug is caused by the incorrect command being executed to retrieve the Fish shell version. The command `echo $FISH_VERSION` simply echoes the value of the environment variable `FISH_VERSION`, which in this case is `'fish, version 3.5.9\n'`. This results in the version output being `'fish, version 3.5.9'` instead of just `'3.5.9'`.

### Fix Strategy
To fix the bug, we need to execute the correct command to fetch the Fish shell version without any extra text. We can modify the command to directly fetch the version without unnecessary information.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(', version ')[1]  # Extract the version number only
    return u'Fish Shell {}'.format(version)
``` 

In this corrected version, we are executing `['fish', '--version']` to directly get the version of the Fish shell without any additional text. We then extract only the version number and return the formatted string `'Fish Shell version'`.