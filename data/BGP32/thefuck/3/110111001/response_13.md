### Explanation:
The error occurs because the `info` function in the `Fish` class is attempting to get the Fish shell version using the command `echo $FISH_VERSION`, but the actual command needed is `fish --version`.

### Strategy for fixing the bug:
1. Update the command within the `Popen` function to `'fish', '--version'`.
2. Modify the `test_info` function to reflect the correct shell version value expected.

### Corrected version of the buggy function:
```python
# The relative path of the buggy file: thefuck/shells/fish.py

# The declaration of the class containing the buggy function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```