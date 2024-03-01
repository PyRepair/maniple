### Analysis:
The buggy function `info` is expected to retrieve the version of the Fish shell by executing a command and extracting the version number. However, the command executed (`echo $FISH_VERSION`) and the way the version is extracted are incorrect. This leads to the incorrect version being returned, causing the test to fail.

### Bug Cause:
1. The command executed (`echo $FISH_VERSION`) does not get the version directly, resulting in the output including extra text.
2. The function does not correctly handle extracting just the version number from the output.

### Bug Fix:
1. Update the command to get just the version (e.g., `fish --version`).
2. Modify the extraction process to ensure only the version number is considered.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    # Extracting version number by splitting the output on comma and extracting the second part
    version = version.split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

Applying these corrections should resolve the issue and make the test pass.