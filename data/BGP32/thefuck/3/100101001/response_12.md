### Analysis
- The `info` function is attempting to get the version of the Fish shell by running a command using `Popen`.
- The `Popen` call is using the command `['fish', '-c', 'echo $FISH_VERSION']` to retrieve the `FISH_VERSION`.
- The test is expecting the output to be `'Fish Shell 3.5.9'`, but the command output is `'fish, version 3.5.9'`.

### Bug
The bug lies in the command used in the `Popen` call. The command used to retrieve the version is not capturing exactly what the test expects.

### Fix
Adjust the command in the `Popen` call to capture only the version number without any additional text.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[2]  # Extract the version number
    return u'Fish Shell {}'.format(version)
``` 

The adjusted command `['fish', '--version']` will provide the version information without any extra text, correcting the bug.