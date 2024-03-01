### Analysis
The error message indicates that the `info` function is returning 'Fish Shell fish, version 3.5.9' instead of the expected 'Fish Shell 3.5.9'. This discrepancy is likely due to the way the output is being processed from the subprocess.

### Potential Error Location
The issue is likely with how the version information is extracted from the subprocess output and formatted into the return string.

### Cause of the Bug
The bug is caused by directly using `proc.stdout.read().decode('utf-8').strip()` to get the version information without considering the actual output format.

### Strategy for Fixing the Bug
To fix the bug, we need to parse the output appropriately to extract only the version number without any extra text.

### Corrected Version of the Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    
    version = proc.stdout.read().decode('utf-8').strip()
    
    # Parse version information to extract only version number
    version = version.split(', ')[1]  # Extract the version number
    
    return u'Fish Shell {}'.format(version)
```

This corrected version parses the version information correctly and extracts only the version number for the return string. This should resolve the issue and pass the failing test.