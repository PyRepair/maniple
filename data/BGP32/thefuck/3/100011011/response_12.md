### Identified Bug:
The bug in the `info` function lies in the way it reads the output from the Popen process. The function expects the output to be in the format `'fish, version X.X.X'`, but the actual output is `'Fish Shell X.X.X'`, causing the assertion to fail.

### Explanation:
The failing test provides a clear view of the issue:
1. The expected output is `'Fish Shell 3.5.9'`.
2. The actual output retrieved from `proc.stdout.read().decode('utf-8').strip()` is `'fish, version 3.5.9'`.

This discrepancy in the format of the expected and actual outputs leads to the assertion error. The function returns a string in the format `u'Fish Shell {}'.format(version)`, but the version extraction from the Popen process is not aligned with this expected format.

### Proposed Fix:
To address the bug, we should modify the function to extract the correct version format from the output of the Popen process. One way to do this is to modify the way we retrieve the version information. We can use a regular expression to extract the version number from the output that matches the expected format.

### Corrected Version:
```python
import re

def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    
    # Extract version number using regex
    match = re.search(r'\d+\.\d+\.\d+', output)
    version = match.group() if match else 'Unknown'
    
    return f'Fish Shell {version}'
```

With this correction, the function will extract the version number in the correct format 'X.X.X' and return the string 'Fish Shell X.X.X', aligning with the expected format and resolving the failing test.