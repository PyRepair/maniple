The bug in the `info` function of the `Fish` class is due to the incorrect command used to retrieve the Fish shell version. The command should be `fish --version` instead of `echo $FISH_VERSION`.

### Bug Explanation:
1. In the buggy function, the `info` function is attempting to get the Fish shell version by executing the command `echo $FISH_VERSION`.
2. The failing test is mocking the output of the command `fish --version` instead of `echo $FISH_VERSION`.
3. As a result, the `info` function reads `'fish, version 3.5.9'` from the mocked output and tries to format it as `'Fish Shell fish, version 3.5.9'`.
4. The assertion in the test compares `'Fish Shell fish, version 3.5.9'` with `'Fish Shell 3.5.9'`, leading to the AssertionError.

### Fix Strategy:
Update the command in the `Popen` function call from `['fish', '-c', 'echo $FISH_VERSION']` to `['fish', '--version']` to correctly fetch the Fish shell version.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```