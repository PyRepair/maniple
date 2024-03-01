The bug in the provided function is that the `proc.stdout.read()` method is called before waiting for the process to complete, leading to an empty output. This results in an empty `version` variable being returned.

To fix this bug, we need to wait for the process to finish before reading the output. We can achieve this by adding `proc.wait()` before reading the output. 

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    proc.wait()  # Wait for the process to finish
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
``` 

This correction ensures that the process finishes execution before reading the output, providing the correct version of the Fish shell.