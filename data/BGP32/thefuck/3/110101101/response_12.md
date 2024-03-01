## Bug Explanation
The bug in the `info` function of the `Fish` class is related to the incorrect command used to retrieve the Fish shell version. It is using the command `echo $FISH_VERSION`, but the test is looking for the version from the command `fish --version`. This mismatch in the commands results in the function not returning the expected version string.

## Fix Strategy
To fix the bug, we need to update the command used to retrieve the Fish shell version in the `info` function to match the command being checked in the test. We should change the command to `['fish', '--version']` to ensure it aligns with the test's expectations.

## The Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.split()[-1])
``` 

By making this change, the updated `info` function should now properly retrieve the Fish shell version and return the expected value 'Fish Shell 3.5.9'.