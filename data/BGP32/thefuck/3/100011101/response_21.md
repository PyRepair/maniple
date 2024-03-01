## Bug Analysis:
The bug is causing the `info` function in the `Fish` class to return the version string with an incorrect prefix 'Fish Shell'. This is due to the fact that the `version` string retrieved from the `fish` command includes 'fish, version' before the actual version number, resulting in mismatched output.

## Bug Fix Strategy:
To fix the bug, we need to modify the way we extract the version number from the output of the `fish` command. We should only extract the version number itself and not include any additional text in the final output.

## Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].strip()  # Extract only the version number
    return u'Fish Shell {}'.format(version)
```

This corrected version of the function will properly extract the version number from the output of the `fish` command and return the expected output, matching the version number without any additional text.