### Analysis:
The error message indicates that the `info` function is returning an unexpected version string from the Fish shell command. The difference between the expected and actual version strings is due to the content read from the `stdout` of the `Popen` process.

### Potential Error Locations:
The issue could be related to how the version information is being read from the `stdout` of the `Popen` process or the format used to construct the return value.

### Cause of the Bug:
When reading the content from the `stdout` of the `Popen` process, the raw output of the command includes some extra text "fish, version" before the version number. This unexpected text causes the version string to be formatted incorrectly in the return value.

### Strategy for Fixing the Bug:
To fix the bug, we need to correctly extract the version number from the output of the Fish shell command and use it to construct the return value without any additional text.

### Corrected Version:
Here is the corrected version of the `info` function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()  # Extract version number only
    return u'Fish Shell {}'.format(version)
```

By splitting the version string based on the comma and extracting the second part (the version number) using `.split(',')[1].strip()`, we can obtain only the version number and ignore the extra text. This corrected version should now return the expected "Fish Shell 3.5.9" value.