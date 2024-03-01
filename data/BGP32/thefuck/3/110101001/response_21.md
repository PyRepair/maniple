### Cause of the bug
The bug is caused by the incorrect shell command `'echo $FISH_VERSION'` being used to retrieve the version of Fish shell. This command does not return the correct version string, leading to the `info()` function returning an incorrect value.

### Strategy for fixing the bug
To fix the bug, we need to change the shell command used to retrieve the Fish shell version. We should use `'fish --version'` instead of `'echo $FISH_VERSION'`.

### Corrected version of the buggy function
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```