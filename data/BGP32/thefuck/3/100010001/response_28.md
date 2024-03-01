### Analysis:
- The buggy function `info` is attempting to get the version of the Fish shell by invoking a subprocess using `Popen`.
- The error message indicates that the expected result is `'Fish Shell 3.5.9'` but the actual result is `'Fish Shell fish, version 3.5.9'`.
- This discrepancy in the actual and expected results is due to the way the version information is being extracted in the buggy function.

### Bug Cause:
- The buggy function reads the output from the subprocess using `proc.stdout.read().decode('utf-8').strip()`.
- This approach does not properly extract only the version number, resulting in the version information being prefixed with `'fish, version'`.

### Fix Strategy:
- To fix the bug, we need to correctly parse the captured output to extract only the version number without any extra information.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_info = proc.stdout.read().decode('utf-8').strip()
    version = version_info.split(",")[1].strip().split()[1]
    return u'Fish Shell {}'.format(version)
```

### Explanation:
- In the corrected version, we split the version_info by the comma `,` and then extract the second part of the split string.
- Further, we split the extracted part by spaces and take the second element, which is the actual version number.
- This ensures that only the version number without any extra information is used while formatting the final output string.