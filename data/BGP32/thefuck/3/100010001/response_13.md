### Analysis:
The error message indicates an assertion error where the expected output of the `shell.info()` function does not match the actual output. The expected output is `'Fish Shell 3.5.9'` while the actual output is `'Fish Shell fish, version 3.5.9'`. This discrepancy suggests that the version extraction from the `Popen` process output is incorrect.

### Bug Location:
The bug is likely located in the way the version is extracted from the output of the `Popen` subprocess call.

### Cause of the Bug:
The bug is caused by not properly handling the output retrieved from the `Popen` subprocess call. The extracted version contains additional text `fish, version` which is not needed in the final output. This additional text is causing the assertion error.

### Strategy for Fixing the Bug:
To fix the bug, we need to properly extract and manipulate the version string extracted from the output of the `Popen` subprocess call. We need to remove the unnecessary text `fish, version` and only keep the version number when formatting the output.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].strip()  # Extract only the version number
    return u'Fish Shell {}'.format(version)  # Format the output with the extracted version number
```

In the corrected version, we split the extracted version by comma and retrieve the second part which contains the version number. This version number is then used to format the final output.This modification should resolve the bug and make the function return the correct version of the Fish shell.