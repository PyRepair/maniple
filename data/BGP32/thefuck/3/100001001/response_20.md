### Explanation:
The issue with the provided function is that it reads the stdout of the Popen process without waiting for it to finish, leading to incomplete or incorrect output reading.

### Strategy for fixing the bug:
To fix the bug, we need to wait for the Popen process to finish and then read the output. This can be achieved by calling `communicate()` on the Popen object, which will wait for the process to finish and then return a tuple containing the stdout and stderr data. We can then extract the stdout data from the tuple.

### Corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    stdout, _ = proc.communicate()
    version = stdout.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
``` 

By using `communicate()` to wait for the process to finish before reading the output, the corrected function will ensure that the version information is correctly extracted from the stdout.