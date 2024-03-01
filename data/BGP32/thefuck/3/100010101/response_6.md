### Analysis
- The error message indicates that the function is not correctly extracting the version number from the command output. The expected version number is '3.5.9', but the function is including extra characters like 'fish, version'.
- The function is using `echo $FISH_VERSION` to extract the version number. This command is returning the version along with the shell name, leading to the incorrect result.

### Bug
The bug is caused by the incorrect parsing of the command output. The function is not extracting only the version number from the output string.

### Fix
To fix the bug, we need to modify how we extract the version number from the command output. We should only consider the version number part and remove any additional text.

### Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[-1]
    return u'Fish Shell {}'.format(version)
``` 

This corrected function will extract only the version number from the output and return the expected result.