### Analysis:
- The error message indicates that the extracted version from the subprocess output is not being processed correctly within the `info` function of the Fish shell.
- The assertion failure is due to the incorrect comparison between the expected version string ('Fish Shell 3.5.9') and the processed version string ('Fish Shell fish, version 3.5.9').

### Error Location:
- The bug lies in how the extracted version is being manipulated and formatted within the `info` function.
- The `u'Fish Shell {}'.format(version)` statement is generating the unexpected version string that causes the assertion failure.

### Bug Cause:
- The incorrect interpretation of the extracted version string ('fish, version 3.5.9') is leading to the assertion failure.
- The version should be extracted and parsed correctly to match the expected format.

### Fixing the Bug:
To fix the bug, we need to modify how the version is extracted and processed within the `info` function. Specifically, we need to remove the 'fish, version' prefix from the extracted version and only keep the version number.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().replace('fish, version', '').strip()
    return u'Fish Shell {}'.format(version)
```

By using the `replace('fish, version', '')`, we remove the unwanted prefix from the extracted version, leaving only the version number itself. This corrected version should now pass the failing test.