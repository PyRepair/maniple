### Bug Explanation
The bug in the `info` function of the `Fish` class lies in the command used to retrieve the Fish shell version. The command `'echo $FISH_VERSION'` does not actually return the version number directly, resulting in the version being extracted as `'fish, version 3.5.9'` rather than just `'3.5.9'`. This causes the assertion to fail because the expected output is `'Fish Shell 3.5.9'`, but the actual output contains unnecessary text.

### Fix Strategy
To fix the bug, the command executed by `Popen` should be changed to `'fish --version'` which explicitly requests the version of the Fish shell, giving us the version number directly.

### Corrected Version
```python
# The declaration of the class containing the corrected function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

By changing the command to `'fish --version'`, the corrected function retrieves the correct shell version directly without any additional text, fixing the bug.