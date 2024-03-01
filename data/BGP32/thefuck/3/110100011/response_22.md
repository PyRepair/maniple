### Analysis:
- The buggy function `info` in the `Fish` class is using the command `echo $FISH_VERSION` to get the version of Fish shell, but in the failing test, the expected output is `fish, version 3.5.9` which is not matching with the output of the command used in the `info` function.
- The failing test is expecting the command `['fish', '--version']` to be used in `Popen`, but the actual command used is `['fish', '-c', 'echo $FISH_VERSION']`.

### Bug Cause:
- The bug is caused because the command used in the `info` function to get the Fish shell version does not match the expected output used in the failing test.

### Fix Strategy:
- Modify the command used in the `info` function to `['fish', '--version']` to match the expected output in the failing test.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

By changing the command to `['fish', '--version']`, the `info` function will now correctly extract the Fish shell version and pass the failing test mentioned in the GitHub issue.