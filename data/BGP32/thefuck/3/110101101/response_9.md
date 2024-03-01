### Bug Explanation:
The bug in the `info` function lies in the command used to retrieve the Fish shell version. The command `'fish', '-c', 'echo $FISH_VERSION'` is incorrect as it does not actually return the version number. This causes the test to fail because it expects the version number to be retrieved from `proc.stdout.read()`, but the incorrect command returns `'fish, version 3.5.9\n'` instead of just the version number.

### Bug Fix:
To fix the bug, we need to change the command executed by `Popen` to correctly retrieve the Fish shell version. We should use the command `'fish', '--version'` instead. This command will directly return the version number without additional text.

### Corrected Version:
```python
# The corrected version of the buggy function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
```

By correcting the command to `'fish', '--version'`, we can now correctly extract the version number and ensure that the function returns the expected output `'Fish Shell 3.5.9'`.