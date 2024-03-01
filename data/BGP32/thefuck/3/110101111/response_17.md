## Fixing the bug

### Analysis:
- The buggy function `info` in the `Fish` class is attempting to get the Fish shell version by running `echo $FISH_VERSION` through a subprocess. However, it is using the incorrect command `['fish', '--version']` instead.
- The failing test is expecting the version number to be extracted from the output of `echo $FISH_VERSION`, which is not currently implemented correctly in the function.

### Bug Cause:
The bug is caused by the incorrect command used to retrieve the Fish shell version in the `info` function. This results in the function not returning the expected version information and failing the test.

### Strategy for fixing the bug:
- Update the command passed to the subprocess to `['fish', '-c', 'echo $FISH_VERSION']` to correctly extract the Fish shell version.
- Modify the function to process the version number extracted from the correct command output.

### Corrected Function:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

Now, the corrected function should correctly extract the Fish shell version using the `echo $FISH_VERSION` command and return the expected output, passing the failing test.