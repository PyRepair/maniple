### Analysis
1. The buggy function `info` in the `Fish` class is supposed to retrieve the version of the Fish shell by executing a command. However, the command used in the `Popen` call is incorrect.
2. The failing test expects the version number to be extracted from the output of the command and formatted as `'Fish Shell 3.5.9'`.
3. The error occurs due to the incorrect command passed to `Popen`, resulting in an unexpected output format.
4. To fix the bug, the correct command to retrieve the Fish shell version should be passed to `Popen`.
5. The corrected version below modifies the command in the `Popen` call.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return 'Fish Shell {}'.format(version)
``` 

By changing the command to `['fish', '--version']`, we ensure that the version number is correctly extracted from the output and formatted as `'Fish Shell 3.5.9'`.