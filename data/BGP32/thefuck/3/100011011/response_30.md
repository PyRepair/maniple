### Identified Bug:
The bug in the `info` function lies in how it extracts the version information from the `stdout` of the `Popen` process. The current implementation is extracting more than just the version number from the output, causing the assertion error in the failing test.

### Cause of the Bug:
The bug is caused by not correctly parsing the version output obtained from the `Popen` process. The current implementation is reading 'fish, version 3.5.9' instead of just '3.5.9' which results in the assertion failure.

### Strategy for Fixing the Bug:
To fix the bug, we need to modify the way the version string is extracted from the output of the `Popen` process. Specifically, we need to extract only the version number from the output and then format it in the desired way for the function output.

### Corrected Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    
    # Extracting the version number from the version output
    version = version_output.split(' ')[-1]
    
    return u'Fish Shell {}'.format(version)
```

By splitting the version output string on spaces and extracting the last element, we can accurately obtain just the version number from the output. This corrected version should now pass the failing test and address the issue reported on GitHub.