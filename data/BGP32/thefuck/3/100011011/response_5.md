### Analysis:
The buggy function `info` in the `fish.py` file is supposed to return the name and version of the Fish shell. The issue seems to be with the retrieval and formatting of the Fish shell version. The failing test indicates that the function is returning the version as `'fish, version 3.5.9'` instead of just `'3.5.9'`.

The provided runtime values and types show that the version extracted from the output of the command includes unnecessary text ('fish, version') which needs to be stripped before formatting the output.

### Bug Cause:
The bug occurs because the function `info` is directly using the output from the command `echo $FISH_VERSION` without stripping the unnecessary text. This leads to the unexpected version format and causes the test to fail.

### Fix Strategy:
To fix the bug, we need to modify the function to extract only the version number from the output of the Fish shell command before formatting the output string.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

In the corrected version:
- Extract the output from the command into `version_output`.
- Split the `version_output` by ',' and select the second part to extract only the version number.
- Strip any extra white spaces from the extracted version.
- Format the output string as 'Fish Shell <version>'.

This corrected version should now return the correct version format and pass the failing test.