The bug in the provided function `info` is that the command `echo $FISH_VERSION` is being used to extract the Fish shell version, but the test is expecting the output of `fish --version` command.

### Cause of the Bug:
The function is executing the wrong command to get the version of the Fish shell, resulting in a mismatch between the expected version `'Fish Shell 3.5.9'` and the actual version `'fish, version 3.5.9'`.

### Fix Strategy:
Modify the command executed by `Popen` to `fish --version` to correctly extract the version of the Fish shell.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(', version ')[1])
``` 

By making this change, the function now correctly extracts the Fish shell version using the `fish --version` command, satisfying the expectations of the test and fixing the bug.