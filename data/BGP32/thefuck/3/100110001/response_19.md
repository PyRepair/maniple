### Analysis:
1. The `info` function takes the output of running `echo $FISH_VERSION` command as the version of the Fish Shell, but the actual version output is `fish, version 3.5.9`.
2. The test code sets the expected output as `'Fish Shell 3.5.9'`.
3. The error message highlights the comparison difference between the shell info result and the expected value.
4. The bug is due to incorrect handling and extraction of the version from the command output in the `info` function.

### Strategy for fixing the bug:
1. Update the `info` function to properly extract the version of the Fish Shell from the command output 'fish, version 3.5.9'.
2. Modify the string processing to extract only the version information and format the output as `'Fish Shell <version>'`.

### Corrected Version of the Bug:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').split(', version ')[1].strip()
    return u'Fish Shell {}'.format(version)
``` 

In the corrected version:
- The command used to get the version is updated to `['fish', '--version']` to fetch the correct version information.
- The version is extracted using `split(', version ')[1]` to get only the version number.
- The format of the return value is modified as `'Fish Shell {}'.format(version)` to match the expected output.

This corrected version should now pass the failing test.