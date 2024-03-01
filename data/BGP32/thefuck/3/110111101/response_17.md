### Bug Explanation
The bug in the `info()` function arises from the way the version is extracted from the output of the `fish --version` command. The current implementation is using the `echo $FISH_VERSION` command, which is not the correct way to retrieve the version information. This leads to the incorrect assertion failure in the test, where the expected version is `'3.5.9'` but the retrieved version is `'fish, version 3.5.9'`.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the command used to retrieve the version information correctly from the `fish --version` command output. By updating the command to get the correct version format, we can ensure that the test passes successfully.

### Corrected Version of the Function
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
``` 

By using the corrected version of the function provided above, the `Fish Shell 3.5.9` version can be correctly extracted from the output of the `fish --version` command, and the test should pass without any assertion errors.