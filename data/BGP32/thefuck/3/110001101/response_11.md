### Strategy for fixing the bug
The bug seems to be related to the incorrect extraction of the version string from the output of the `fish -c 'echo $FISH_VERSION'` command. The current implementation is not properly handling the output. To fix this bug, we need to ensure that we correctly extract the version string from the output of the command.

### Corrected version of the function
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The corrected version of the class containing the buggy function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        # Extract the version from the output considering 'fish, version X.X.X' format
        version = version.split(' ')[-1]
        return u'Fish Shell {}'.format(version)
```

By splitting the output of the command and extracting the version from the last element of the splitted list, we ensure that we obtain just the version string. This corrected version should now correctly extract and return the version of the Fish shell.