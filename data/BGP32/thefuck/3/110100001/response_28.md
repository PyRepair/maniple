### Analysis:
1. The buggy function `info` in the `Fish` class is trying to get the version of the Fish shell by executing a command using `Popen`.
2. The test function `test_info` is mocking the `Popen` object and setting the expected output to be `b'fish, version 3.5.9\n'`.
3. The bug is likely due to the incorrect command being passed to `Popen` in the `info` function.
4. To fix the bug, we need to change the command passed to `Popen` from `['fish', '-c', 'echo $FISH_VERSION']` to `['fish', '--version']` to match the expected command in the test.

### Bug Fix:
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

With this fix, the `info` function in the Fish class should correctly fetch the version of the Fish shell, and the test case `test_info` should pass without any issues.