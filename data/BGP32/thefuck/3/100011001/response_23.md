### Analysis
The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`. This suggests that the `version` variable is not correctly extracted from the output of the `Popen` process.

The bug seems to be in the way the output of `Popen` is read and processed to extract the version information.

### Bug
The bug lies in the line where the `version` is extracted from the output of `proc.stdout.read()`. The version information is extracted directly without handling the additional text `'fish, version'`.

### Fix
To fix the bug, we need to extract the version information correctly by removing the extra text `'fish, version'` from the output. One way to do this is by splitting the output based on the delimiter `', version'` and then taking the second part as the version.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(', version ')[1]
    return u'Fish Shell {}'.format(version)
``` 

This fix will correctly extract the version information from the output and return it in the expected format.