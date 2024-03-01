### Bug Explanation
The bug in the `info` function is caused by the fact that the command used to retrieve the Fish shell version is incorrect. The command used is `echo $FISH_VERSION` which returns a string like `'fish, version 3.5.9'` instead of just the version number. This causes the assertion in the test function to fail as the expected output for the `info` function is just the version number without any additional text.

### Bug Fix Strategy
To fix the bug, the command used to retrieve the Fish shell version should be changed to `fish --version` which will return just the version number without any additional text.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
``` 

By updating the command in the `Popen` call to `['fish', '--version']` and modifying the version extraction to just get the version number, the corrected version should now pass the failing test.