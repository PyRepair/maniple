## Analysis
The error message indicates that the `info` method of the `Fish` class in the `fish.py` file is returning the wrong format of the version. The expected version is '3.5.9' but it is being returned as 'fish, version 3.5.9'. This mismatch is causing the assertion error. 

## Error Location
The issue is likely in the formatting of the version returned by the `info` method of the `Fish` class. The function is not processing the output of the command properly.

## Bug Cause
The bug in the original function lies in how the stdout response of the `Popen` call is read and processed. The `proc.stdout.read().decode('utf-8').strip()` method is directly reading the stdout response as bytes, decoding it as UTF-8, and then stripping any extra whitespace. This direct processing is causing the prefix 'fish, version' to stay in the version string, leading to the incorrect format.

## Strategy for Fixing the Bug
To fix the bug, we need to parse the actual version number from the stdout response correctly, without the extra text 'fish, version'. One way to achieve this is by splitting the response on ' ' (space) characters and extracting the last element which corresponds to the version number.

## Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(' ')[-1]  # Extract version from the response
    return u'Fish Shell {}'.format(version)
```

This corrected version of the `info` method processes the stdout response properly to extract only the version number without any additional text. It should now return the correct format 'Fish Shell 3.5.9' as expected.