The bug in the provided function is that it is attempting to read from the stdout of the Popen process using `proc.stdout.read()` before calling `proc.communicate()` to allow the process to finish and return the output.

### Cause of the Bug:
The bug occurs because the Popen process is not being waited on to finish before reading the stdout. As a result, the output may not be available at the time of reading, leading to an empty string being returned.

### Strategy for Fixing the Bug:
To fix the bug, we need to modify the function to wait for the process to finish before reading from its stdout. This can be achieved by calling `proc.communicate()` to ensure the process has completed.

### Corrected Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    proc.communicate()  # Wait for the process to finish
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By adding `proc.communicate()` before reading from `proc.stdout`, we ensure that the process has completed and the output is available to be read.