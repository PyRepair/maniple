## Bug Explanation
The bug in the `info` function is caused by passing the incorrect command `echo $FISH_VERSION` to get the Fish shell version. The correct command to get the Fish shell version is `fish --version`, which was confirmed in the failing test by asserting `Popen.call_args[0][0] == ['fish', '--version']`.

## Bug Fix
To fix the bug, we need to update the command used to get the Fish shell version in the `info` function to `fish --version`.

## The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
``` 

By using the correct command `['fish', '--version']`, we can retrieve the Fish shell version correctly and strip the output to get only the version number. This correction should now pass the failing test and return the expected version number.