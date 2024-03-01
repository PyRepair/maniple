## Bug Explanation
The bug in the `info` function stems from the command used to retrieve the Fish shell version. The command `echo $FISH_VERSION` is incorrect and does not match the command being checked in the test function `['fish', '--version']`. It results in the incorrect version information being extracted, leading to the failing test.

## Fix Strategy
To fix the bug, the correct command to fetch the Fish shell version should be used. Instead of `echo $FISH_VERSION`, the function should execute `fish --version` to get the proper version information.

## The corrected version of the buggy function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
``` 

By using `['fish', '--version']` in the Popen command, the function now correctly retrieves the Fish shell version and formats it appropriately to pass the failing test.