## Bug Cause

The bug is caused by the incorrect command used to retrieve the version of the Fish shell in the `info` function. The actual output 'Fish Shell fish, version 3.5.9' does not match the expected output 'Fish Shell 3.5.9', indicating that the function is not obtaining the correct version of the shell. This results in a failing test and an assertion error.

## Approach to Fix the Bug

To fix the bug, the command used to retrieve the version of the Fish shell should be updated to ensure that the correct version is retrieved and parsed from the output.

## The Corrected Code

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(' ')[2]
    return u'Fish Shell {}'.format(version)
```

In the corrected code, the command to retrieve the version of the Fish shell has been updated to use `['fish', '--version']` instead of 'echo $FISH_VERSION'. This command will now correctly return the version of the Fish shell, which is then parsed and formatted to match the expected output. This modification resolves the issue and ensures that the `info` function returns the correct version of the Fish shell.