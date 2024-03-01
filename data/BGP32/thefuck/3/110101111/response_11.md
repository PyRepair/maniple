## Fixing the bug

### Issue:
The buggy function `info` in the `Fish` class is not reading the correct output from the `fish -c 'echo $FISH_VERSION'` command due to incorrect handling of the output. This results in the test failing because the expected version is not being correctly extracted and formatted.

### Strategy for fixing the bug:
1. Modify the command passed to `Popen` to `['fish', '-v']` to correctly retrieve the Fish Shell version.
2. Update the code to parse the version information from the output of the command in the correct format.

### Corrected Version:
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The corrected version of the class containing the buggy function
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-v'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split()[-1]  # Extract the version number from the output
        return u'Fish Shell {}'.format(version)
```

After making these changes, the `info` function should correctly retrieve the Fish Shell version using the `fish -v` command and return it in the expected format, fixing the bug and ensuring that the failing test passes.

This updated version should resolve the issue reported on GitHub related to the use of the `thefuck -v` command hanging the Fish Shell initialization with the Oh-My-Fish plugin.