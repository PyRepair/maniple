### Bug Analysis
The `info` function is intended to fetch the version of the Fish shell by executing a command and extracting the version from the output. However, the bug lies in how the version is being extracted from the output. The current implementation is extracting the entire output line (`fish, version 3.5.9`) instead of just the version number (`3.5.9`).

### Bug Fix
To fix the bug, we need to modify the code to extract only the version number from the output. We can achieve this by splitting the output and taking only the last part, which represents the version number.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split(", version")[-1].strip()
    return u'Fish Shell {}'.format(version)
``` 

With this corrected version, the function should now correctly extract only the version number from the output and return it in the expected format.