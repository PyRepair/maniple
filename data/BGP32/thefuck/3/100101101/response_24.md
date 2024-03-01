### Analysis:
The bug in the `info` function lies in the command used to retrieve the Fish shell version. The command `echo $FISH_VERSION` is incorrect as it does not extract the correct version information. Additionally, the test is looking for `['fish', '--version']` as the command, which is not being used in the function.

### Bug Cause:
The function uses the incorrect command to retrieve the Fish shell version, leading to the incorrect version being returned. The test case expects a different command format that is not being used in the function.

### Strategy for Fixing the Bug:
1. Update the command in the Popen call to `['fish', '--version']` to correctly retrieve the Fish shell version.
2. Trim the extracted version string to remove unnecessary parts like "fish, version" from the output.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.replace('fish, version ', '')  # Remove unnecessary parts
    return u'Fish Shell {}'.format(version)
```

After correcting the function as mentioned above, the function should now correctly retrieve the Fish shell version using the appropriate command format and manipulate the output to provide just the version number. This will ensure that the function passes the failing test case.