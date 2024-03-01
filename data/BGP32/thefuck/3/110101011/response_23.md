### Identified Bug:
The bug in the `info` function of the `Fish` class is due to the incorrect command being used to retrieve the Fish shell version. In the test function, `Popen.call_args[0][0]` expects `['fish', '--version']` but the actual command used is `['fish', '-c', 'echo $FISH_VERSION']`. This discrepancy causes the test to fail.

### Strategy for Fixing the Bug:
To fix the bug, the command passed to `Popen` should be updated to `['fish', '--version']` so that it matches the expected command in the test function.

### Corrected Version of the Function:
```python
# The corrected version of the function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

By updating the command passed to `Popen` in the `info` function of the `Fish` class, the bug should be fixed, and the test `test_info` should pass successfully.