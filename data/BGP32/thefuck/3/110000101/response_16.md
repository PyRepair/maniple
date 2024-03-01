### Analysis
The bug in the provided function is that it is not waiting for the completion of the subprocess before trying to read from its stdout. This can lead to an empty read result if the subprocess has not finished executing.

### Strategy for fixing the bug
To fix the bug, we need to wait for the subprocess to finish executing before attempting to read from its stdout.

### The corrected version of the function
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        proc.wait()  # Wait for the subprocess to finish
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```