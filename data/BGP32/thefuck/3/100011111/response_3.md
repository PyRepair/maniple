### Analysis
The bug in the `info` function stems from the fact that the returned version string contains extra text (`fish, version`) that needs to be stripped out. The test case is failing because it directly compares the expected output ('Fish Shell 3.5.9') with the actual output ('Fish Shell fish, version 3.5.9').

### Bug Cause
The bug is caused by not properly parsing the version number from the command output. It is extracting the entire output string instead of just the version number.

### Fix Strategy
To fix the bug, we need to modify the logic to extract only the version number from the retrieved output.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(' ')[-1]  # Extracting only the version number
    return u'Fish Shell {}'.format(version)
``` 

By splitting the output based on spaces and taking the last element, we can extract just the version number from the command output, leading to the correct return value.