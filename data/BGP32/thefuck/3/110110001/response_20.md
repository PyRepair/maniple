### Analysis:
- The buggy function `info` in the `Fish` class is intended to return the name and version of the current shell, which in this case is the Fish shell.
- The test function `test_info` is mocking the behavior of `Popen` to return `b'fish, version 3.5.9\n'`, expecting the function to extract the version and format it as `'Fish Shell 3.5.9'`.
- The bug seems to be related to the command used to get the version (`echo $FISH_VERSION` vs. `fish --version`).
- The error message indicates that the actual output includes extra text `fish,` before the version number, causing the assertion to fail.

### Explanation:
- The bug is caused by the incorrect command `echo $FISH_VERSION` being used to extract the Fish shell version.
- The output of this incorrect command includes extra text `fish, version` which is not handled properly in the formatting.

### Strategy for fixing the bug:
- Change the command used in `Popen` to `['fish', '--version']` to correctly get the version of the Fish shell.
- Modify the way the version is extracted to only include the version number.

### Corrected Version:
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split(', version')[-1]  # Extract only the version
        return f'Fish Shell {version.strip()}'
``` 

After making this correction, the test should pass without the extra text `fish,` causing any issues.