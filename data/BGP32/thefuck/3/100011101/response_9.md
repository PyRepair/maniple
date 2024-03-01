### Analysis:
- The error message indicates an assertion failure between the actual output of the `info` function and the expected output.
- The expected output is `'Fish Shell 3.5.9'` while the actual output is `'Fish Shell fish, version 3.5.9'`.
- The problem seems to be related to the extraction of the version number from the command output.

### Bug:
The buggy function is not properly extracting the version number from the command output. It is including unnecessary characters like `'fish, version'` in the output instead of just extracting the version number.

### Fix:
To fix the bug, we need to modify the code so that it correctly extracts just the version number from the output.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    
    # Extract only the version number
    version_number = version.split()[-1]
    
    return u'Fish Shell {}'.format(version_number)
``` 

By modifying the code to extract only the version number from the output, the corrected version should now return `'Fish Shell 3.5.9'`, satisfying the expected output.