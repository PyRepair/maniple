The bug in the provided function is that it is trying to read from the `proc.stdout` before waiting for the process to finish. This can lead to incorrect or missing output from the command being executed.

To fix this bug, we need to wait for the process to finish before reading from `proc.stdout`.

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

By adding `proc.wait()` before reading from `proc.stdout`, we ensure that the process has finished executing and the output is available to be read. This correction should fix the bug in the function.