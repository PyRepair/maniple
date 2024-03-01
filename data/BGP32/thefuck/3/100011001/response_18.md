### Bug Analysis:
- The `info` function is supposed to return the version of the Fish Shell by running a command `fish -c 'echo $FISH_VERSION'`. However, the output is not being processed correctly, resulting in the error message showing the entire output instead of just the version number.
- The error message indicates that the expected result is `'Fish Shell 3.5.9'` but the function is returning `'Fish Shell fish, version 3.5.9'`.

### Bug Fix:
To fix the bug, we need to process the command output to extract only the version number and return it accordingly.

### Corrected Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].strip()  # Extract only the version number
    return u'Fish Shell {}'.format(version)
``` 

By splitting the output of the command at the comma and taking the second part (which is the version number), we can ensure that the function returns only the version number and not the entire output string.