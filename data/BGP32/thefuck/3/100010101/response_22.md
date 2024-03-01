### Analysis
The error message indicates that the function is returning a string with unexpected content, which is causing the test to fail. The expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`. This suggests that the function is not correctly extracting the version number from the command output.

### Bug
The bug lies in the way the function is parsing the output of the command `echo $FISH_VERSION`. It is not correctly isolating the version number from the entire output string.

### Fix
To fix the bug, we need to modify the way the function processes the output to only extract the version number portion.

### The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(', version ')[-1].strip()  # Extract only the version number
    return u'Fish Shell {}'.format(version)
``` 

By splitting the output string at `', version '` and taking the last part, we ensure that we extract only the version number. This correction should now return the expected output `'Fish Shell 3.5.9'` and pass the failing test.