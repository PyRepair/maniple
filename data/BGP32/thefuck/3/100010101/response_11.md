### Analysis
The error message indicates that the output of the `shell.info()` function does not match the expected `'Fish Shell 3.5.9'`. The test input is mocking the `Popen` object to return `b'fish, version 3.5.9\n'`, which results in the incorrect output when the function extracts the version number.

### Bug
The issue lies in how the function extracts the version number from the output of the `Popen` command. The function currently extracts the version information directly from the output without parsing properly, leading to the incorrect format in the return value.

### Fix
To fix the bug, we need to correctly parse the version number from the output of the `Popen` command by splitting the result and extracting the version number. 

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(', version ')[-1]
    
    return u'Fish Shell {}'.format(version)
```

This corrected version reads and decodes the output, splits it by `', version '`, and extracts the version number to correctly format the return value.