### Analysis
The bug in the `info` function is caused by the incorrect use of the command to get the version of Fish shell (`echo $FISH_VERSION` instead of `fish --version`). This results in the function not correctly extracting the version information and causing the test to fail.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the command being used to retrieve the Fish shell version. By replacing `echo $FISH_VERSION` with `fish --version`, we will be able to properly capture the version information returned by Fish shell and make the function return the expected output.

### Corrected Version of the Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```