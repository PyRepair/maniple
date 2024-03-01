### Bug Explanation
The bug in the `info` function lies in the fact that the command used to retrieve the Fish shell version is incorrect. The command `echo $FISH_VERSION` is used, but the test is expecting the version to be retrieved using `fish --version`.

### Bug Fix Strategy
To fix the bug, we need to update the command used to retrieve the Fish shell version to `fish --version`.

### Corrected Version
```python
# The relative path of the buggy file: thefuck/shells/fish.py

# The declaration of the class containing the buggy function
class Fish(Generic):

    # Corrected version of the buggy function
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
``` 

After applying the correction, the test should pass as the function now retrieves the Fish shell version using the correct command.