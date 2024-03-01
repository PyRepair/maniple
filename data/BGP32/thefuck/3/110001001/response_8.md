### Bug Explanation
The bug in the `info` function is due to not properly waiting for the `Popen` process to finish before reading from its output. This causes the function to read the output before it is available, leading to incorrect or missing values.

### Fix Strategy
To fix the bug, we need to wait for the `Popen` process to complete before reading its output. We can achieve this by using the `.communicate()` method of the `Popen` object, which will wait for the process to finish and then return the output data.

### Corrected Version
Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    stdout, _ = proc.communicate()
    version = stdout.decode('utf-8').strip()
    return 'Fish Shell {}'.format(version)
``` 

This fixed version ensures that the function properly waits for the `Popen` process to complete before reading the output data, preventing any issues related to reading incomplete or missing values.