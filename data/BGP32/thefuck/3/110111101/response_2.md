### Bug Explanation
The bug in the `info` function of the `Fish` class arises from the inconsistency between the expected and actual versions of the Fish shell. The function is expecting the version to be in the format `'3.5.9'` but is actually receiving it in the format `'fish, version 3.5.9'`. This discrepancy leads to the assertion error in the failing test.

### Fix Strategy
To fix this bug, we need to modify the way we extract the version from the output of the `fish -c 'echo $FISH_VERSION'` command. We should extract only the version number without any additional text.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().replace('fish, version ', '')
        return u'Fish Shell {}'.format(version)
``` 

By modifying the line `version = proc.stdout.read().decode('utf-8').strip()` to `version = proc.stdout.read().decode('utf-8').strip().replace('fish, version ', '')`, we extract only the version number without the extraneous text. This change ensures that the version retrieved matches the expected format, fixing the bug.