### Bug Explanation
The bug in the `info` function lies in the command used to retrieve the Fish Shell version. The command `'echo $FISH_VERSION'` does not actually output the version number. Instead, we should use `'fish --version'`.

### Bug Fix
To fix the bug, we need to change the command in the `Popen` call to `'fish --version'`.

### Corrected Version
```python
# The relative path of the buggy file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
```