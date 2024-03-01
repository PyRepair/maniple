### Explanation:
The bug in the provided function lies in how the `Popen` process is being handled. The function is not waiting for the process to complete before reading its output, leading to incorrect or missing results.

### Strategy for Fixing the Bug:
To fix the bug, you should wait for the `Popen` process to complete before reading its output. This can be accomplished by adding a call to `proc.wait()` before reading from `proc.stdout`. 

### Corrected Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    proc.wait()  # Wait for the process to complete
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
``` 

By adding `proc.wait()` before reading from `proc.stdout`, the function will correctly wait for the process to finish executing before retrieving the output, ensuring the correct version of the Fish Shell is returned.