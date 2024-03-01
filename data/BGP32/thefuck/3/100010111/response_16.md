## Analysis
The buggy function `info` is attempting to get the version of Fish shell by running the command `fish -c 'echo $FISH_VERSION'`. The bug seems to be related to how the version is extracted from the output of the command.

The error message indicates that the function is returning `'Fish Shell fish, version 3.5.9'` instead of `'Fish Shell 3.5.9'`. This suggests that the version extraction or formatting is incorrect.

The expected input parameter values are provided as `MagicMock` objects, and the expected `version` value is `'3.5.9'`. The function needs to correctly extract this version value.

## Error Cause
The bug is caused by the incorrect formatting of the version string obtained from the command output. The function is not correctly stripping the output to only extract the version number.

## Bug Fix Strategy
To fix the bug, we need to modify the way we extract and format the version number from the output of the command. We should ensure that only the version number is captured without any additional text.

## Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    # Extract only the version number from the output
    version = version.split(',')[-1].strip()
    return u'Fish Shell {}'.format(version)
```

By splitting the version string at the comma (if present) and selecting the last part, we can ensure that only the version number is obtained. This corrected version should now pass the failing test and correctly format the version string.