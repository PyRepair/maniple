## Bug Explanation
The bug is caused by the incorrect command used to get the Fish shell version. In the `info` function, the command `echo $FISH_VERSION` is being used to get the Fish shell version, but in the failing test, the expected command is `fish --version`. This mismatch in the commands results in the `info` function returning an incorrect version string.

## Bug Fix Strategy
To fix the bug, we need to update the command used to retrieve the Fish shell version in the `info` function. We should change it to `fish --version` to match the expected command in the failing test.

## Corrected Version
```python
class Fish(Generic):
    
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.replace('fish, version ', ''))
``` 

By updating the command to `fish --version` in the `Popen` call and adjusting the string manipulation to remove the 'fish, version ' prefix from the version string, the corrected version of the `info` function should now return the correct Fish shell version.