### Analysis:
The buggy function `info` in the `Fish` class is supposed to return the version of the Fish shell by executing a command and extracting the version from the output. The error message indicates that the output received from the command includes additional text (`fish, version`) which is not expected, causing the assertion to fail.

### Error Location:
The issue lies in how the version is being extracted from the output of the command. The actual output includes `fish, version` before the version number, causing the incorrect comparison in the test case.

### Bug Cause:
The buggy function `info` reads the output of the command and directly uses `strip()` to remove any leading/trailing whitespaces. However, it does not account for the additional text `fish, version` that is included in the output, leading to an incorrect version extraction.

### Strategy for Fixing the Bug:
To fix the bug, the extraction of the version number from the output needs to be done in a way that considers the extra text present in the output. We can modify the code to split the output based on the comma symbol and extract the version number from the second part of the split.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(' ')[-1]  # Extract version from the last part after splitting by space
    return u'Fish Shell {}'.format(version)
```

By splitting the `output` based on the space character, we extract the version number correctly, which can now be compared accurately in the test case. This correction should resolve the failing test case and the issue reported on GitHub.