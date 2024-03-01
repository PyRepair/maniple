### Explanation:
The bug in the function is caused by not waiting for the `Popen` process to finish before attempting to read from its output. This results in the `proc.stdout.read()` call returning an empty string because the process might not have completed writing to the output stream when the read operation is performed.

### Solution:
To fix this bug, the function should wait for the process to finish before reading its output. One way to achieve this is by adding `proc.wait()` after creating the process using `Popen`.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    proc.wait()
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
``` 

This corrected version ensures that the process has finished executing before attempting to read from its output stream, resolving the bug.