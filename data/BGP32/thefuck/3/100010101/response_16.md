### Analysis
- The buggy function `info` is intended to fetch the version of the Fish shell by invoking a subprocess and capturing the output.
- The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output contains unexpected characters.
- The issue seems to be related to how the version information is being extracted from the subprocess output.

### Bug
The bug is in how the version string is being extracted from the subprocess output. The current implementation is simply calling `strip()` on the output, which is not effectively removing all unwanted characters.

### Fix
To fix the bug, we need to extract the version number more accurately from the subprocess output by considering the actual structure of the output.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].split()[1]
    return u'Fish Shell {}'.format(version)
```

This corrected version enhances the extraction logic by splitting the output based on commas and whitespace to isolate the version number accurately.