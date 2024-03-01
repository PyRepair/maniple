## Analysis
The buggy function `info` is supposed to retrieve the version of the Fish shell by running the command `fish -c 'echo $FISH_VERSION'` and then returning it formatted as 'Fish Shell VERSION'. However, the current implementation is reading the version string incorrectly from the `stdout` of the `Popen` object and not formatting it properly before returning.

The error message indicates that the expected version `'3.5.9'` is not being properly formatted as `'Fish Shell 3.5.9'`. The failing test provides the version string as `'fish, version 3.5.9'`, which suggests that the bug lies in how the version string is retrieved and formatted.

## Bug Cause
The bug is caused by not handling the actual output correctly while reading the stdout of the `Popen` object. The version string retrieved from stdout includes additional text ("fish, version") that needs to be filtered out before it is formatted as "Fish Shell VERSION".

## Fix Strategy
To fix the bug, we need to modify the way the version string is extracted and formatted before returning it. We should extract only the version number from the command output and then format it properly.

## Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(',')[1].strip().split(' ')[1]
    return f'Fish Shell {version}'
```

In the corrected version, we read the output from `proc.stdout` and split it based on the commas. We then extract the version number by further splitting the text and retrieve the second element after splitting on spaces. This way, we ensure that only the version number is included in the final formatted string.