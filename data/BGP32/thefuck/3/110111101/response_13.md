### Bug Analysis:
The buggy function `info` in the `Fish` class is reading the `FISH_VERSION` environment variable using the command `'echo $FISH_VERSION'`, which is not the correct command to get the version of the Fish Shell. The failing test expects the output to be `'Fish Shell 3.5.9'`, but the current implementation is producing `'Fish Shell fish, version 3.5.9'`. This discrepancy is due to the incorrect output parsing and formatting.

### Bug Fix Strategy:
To fix the bug, we need to change the command used to fetch the Fish Shell version and correctly parse the version from the output.

### Corrected Function:
Here is the corrected version of the `info` function in the `Fish` class:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]
        return f'Fish Shell {version}'
```

With this correction, the function will execute the correct command to get the Fish Shell version and correctly parse the output to extract the version number.