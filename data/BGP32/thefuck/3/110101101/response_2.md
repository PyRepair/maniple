### Explanation:
The bug in the `info` function is caused by the mismatch in the command used to retrieve the Fish shell version. The function is currently trying to extract the version using the command `echo $FISH_VERSION`, but the test is expecting the version output from `fish --version`.

### Strategy for fixing the bug:
To fix the bug, we need to update the command used to retrieve the Fish shell version to `fish --version` instead of `echo $FISH_VERSION`.

### Corrected version of the function:
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The corrected version of the info function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[2]
        return u'Fish Shell {}'.format(version)
```

By updating the command to use `fish --version` and extracting the version correctly from the output, the corrected function should pass the failing test and provide the expected output.