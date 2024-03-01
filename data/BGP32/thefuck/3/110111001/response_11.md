### Bug Analysis:
- The `info` function in the `Fish` class is using the command `echo $FISH_VERSION` to retrieve the Fish shell version, but the test is expecting the version to be obtained with `fish --version`.
- The test function is setting the `stdout.read` side effect to `'fish, version 3.5.9\n'`, which is different from what the `info` function is trying to extract (`$FISH_VERSION`).

### Bug Cause:
The `info` function in the `Fish` class is not extracting the Fish shell version correctly. It is using a different command compared to what the test expects, leading to the assertion error.

### Bug Fix:
To fix this bug, we need to update the command used in the `info` function to get the Fish shell version. Additionally, we need to modify the test to match the new command.

### Corrected Version:
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

After making these changes, the `info` function should now correctly extract the Fish shell version, resolving the failing test.