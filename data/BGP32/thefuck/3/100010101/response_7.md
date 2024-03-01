### Analysis
- The buggy function `info` is attempting to get the version of the Fish shell by running a command in a subprocess and reading the output.
- The error message shows that the returned version includes extra text, causing the assertion to fail.
- The expected version value is just the version number without any additional text.

### Bug Cause
- The bug is caused by not properly parsing the output of the subprocess command. In this case, the output includes "fish, version" followed by the actual version number.
- The function is not correctly handling this output format, leading to the extra text being included in the final version string.

### Fix Strategy
- The fix involves modifying the way the output is read and processed. We need to extract only the version number from the output and return it as the final version string.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
    return u'Fish Shell {}'.format(output)
``` 

This corrected version properly extracts the version number from the output of the subprocess command and returns it as the final version string.