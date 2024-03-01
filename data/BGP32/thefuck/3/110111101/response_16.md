### Bug Analysis:
The buggy function `info` in the `Fish` class is not retrieving the correct version information from the `fish` shell command. The test is failing because the expected version number is different from the actual extracted version in the function.

1. **Error Location**:
   - The `Popen` call should use `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']` to get the correct version information.
   - The extraction of version information from the output of the `Popen` process is not correctly formatted.

### Bug Fix Strategy:
To fix the bug and align the function with the expected test behavior:
- Update the command in the `Popen` call to `['fish', '--version']` to get the version information directly.
- Modify the way the version information is extracted from the output to match the expected format '3.5.9'.

### Corrected Version of the Function:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(' ')[-1]
        return 'Fish Shell {}'.format(version)
```

By correcting the function as shown above, the `info` function in the `Fish` class will now extract the version information correctly from the `fish` shell command output, and the test should pass with the expected version '3.5.9'.