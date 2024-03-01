### Analysis:
1. The buggy function `info` in the `Fish` class is attempting to get the Fish Shell version by running the command `fish -c 'echo $FISH_VERSION'`.
2. The failing test `test_info` expects the shell version to be extracted from the command output, but the command being run is `fish --version` instead of `fish -c 'echo $FISH_VERSION'`.
3. The failing test is due to the mismatch between the expected command output and the actual command being executed in the `info` function.
4. To fix the bug, we need to update the command run in the `info` function to `fish --version` instead of `fish -c 'echo $FISH_VERSION'`.

### Bug Fix:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

By updating the `Popen` command to `['fish', '--version']`, the corrected version of the function should now extract the correct Fish Shell version from the output, resolving the bug and passing the failing test.