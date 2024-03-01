The bug in the provided function `info` is related to how the version information is extracted from the output of the `fish` command. The current implementation includes the text `'fish, version'` in the version string, which is not desired.

### Cause of the Bug:
1. When the `fish` command is executed with the `-c` flag to print the `FISH_VERSION`, the returned output includes the text `'fish, version'` before the actual version number.
2. The function is incorrectly extracting the version information without removing the unwanted text.

### Strategy for Fixing the Bug:
To fix the bug, we need to modify the function to extract only the version number from the command output by removing the unwanted text `'fish, version'`.

### Corrected Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version_text = 'fish, version'
    if version.startswith(version_text):
        version = version.replace(version_text, '').strip()
    return u'Fish Shell {}'.format(version)
```

By checking if the version string starts with `'fish, version'`, we can remove this part of the string to get the actual version number. This corrected version of the function should now return the expected version number without the unwanted text.