### Explanation:
The bug in the provided function is that it's not correctly extracting the version of the Fish Shell. The function is currently returning the full string `fish, version 3.5.9` instead of just the version number `3.5.9`.

The issue lies in the line:
```python
version = proc.stdout.read().decode('utf-8').strip()
```
The `proc.stdout.read()` is reading the entire output string `fish, version 3.5.9` instead of just the version number part.

### Bug Fix Strategy:
To fix the bug, we need to extract only the version number from the output string. One way to do this is by splitting the output string on the comma and then fetching the version number part.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    
    # Splitting the output string on comma and extracting the version number
    version = output.split(',')[1].strip()
    
    return u'Fish Shell {}'.format(version)
``` 

This corrected version should properly extract and return the version number of the Fish Shell.