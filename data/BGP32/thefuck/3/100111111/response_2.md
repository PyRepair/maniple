### Analysis
- The buggy function `info` in `fish.py` is using `Popen` to execute the command `fish -c 'echo $FISH_VERSION'` to get the version of the Fish shell.
- The test function `test_info` in `test_fish.py` expects the version to be only the version number without the additional text.
- The failing test is due to the mismatch in the expected and actual output of the `info` function related to the version number.
- The error message highlights the difference in the format of the shell version.
- The GitHub issue suggests that the version information issue is causing problems in some cases.

### Error
The bug is in how the version is retrieved and formatted in the `info` function. It includes the text "fish, version" in the version string, which is not expected.

### Fix Strategy
To fix the bug, we need to modify the `info` function in `fish.py` to extract only the version number from the shell output and format it correctly.

### Corrected Version

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    # Parse the version string to extract only the version number
    version = version.split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

After making this correction, the function should extract and format the version number correctly, resolving the failing test and meeting the expected input/output values.