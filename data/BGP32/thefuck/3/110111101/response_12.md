### Buggy function analysis
The buggy `info` function in the `Fish` class is meant to extract the version number of the Fish shell. It uses a subprocess to execute a command in Fish shell to retrieve the version information. However, the command used (`echo $FISH_VERSION`) does not match the expected output (`fish, version 3.5.9`).

### Error identification
- The `info` function is extracting the version information incorrectly, leading to a mismatch between the actual output and the expected output.
- The `Popen` call is using `['fish', '-c', 'echo $FISH_VERSION']` but the test case expects `['fish', '--version']`.

### Bug cause
The bug is caused by not correctly extracting and formatting the Fish shell version information.

### Bug fix strategy
1. Update the `Popen` call to use `['fish', '--version']` to retrieve the correct version information.
2. Remove the unnecessary formatting of the version information (`'fish, version 3.5.9'`) to make it match the expected output (`'Fish Shell 3.5.9'`).

### Corrected code
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
``` 

After making the above changes, the `info` function should now correctly extract the Fish shell version information and format it as expected, passing the failing test case.