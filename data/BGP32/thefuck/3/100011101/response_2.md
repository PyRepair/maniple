### Analysis
- The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output includes the extra `'fish, version '` part.
- The `proc.stdout.read().decode('utf-8').strip()` is not correctly extracting just the version number from the output.
- The actual version extracted is `'fish, version 3.5.9'`, while the expected version is just `'3.5.9'`.

### Bug Cause
- The bug is caused by not properly extracting and formatting the version number from the output of the command `echo $FISH_VERSION`.
- The function should only return the version number without any additional text like `'fish, version '`.

### Fix Strategy
- To fix the bug, we need to modify the code to correctly extract only the version number from the output string.

### The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()  # Get the output string
    # Extract the version number using string manipulation
    version = version_output.split(', ')[1] if ', ' in version_output else version_output
    return u'Fish Shell {}'.format(version)
```

With this corrected version, the function will correctly extract only the version number from the output and return it in the desired format.