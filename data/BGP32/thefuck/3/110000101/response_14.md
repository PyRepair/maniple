### Analysis
The buggy function `info` is attempting to get the version of the Fish shell by running a command using `Popen`, capturing the output, and then returning the version string. The issue seems to be related to how the output is read from the subprocess.

### Potential Error Locations
1. Reading the output from `proc.stdout` without waiting for the process to finish.
2. Incorrectly decoding the output.

### Cause of the Bug
The bug is likely caused by trying to read from `proc.stdout` directly without waiting for the process to finish executing. This can result in an empty output or incomplete data being read, leading to an incorrect version or an empty string.

### Strategy for Fixing the Bug
To fix the bug, we can ensure that we wait for the process to finish executing before attempting to read from `proc.stdout`. Additionally, we should handle any errors that may occur during the process execution.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    proc.wait()  # Wait for the process to finish
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```