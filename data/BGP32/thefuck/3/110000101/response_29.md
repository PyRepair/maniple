### Strategy for fixing the bug
The bug in the provided function is likely due to not waiting for the `Popen` process to finish before reading its output. To fix this issue, we can use the `communicate()` method of the `Popen` object, which waits for the process to finish and returns a tuple of stdout and stderr.

### Corrected version of the function
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        stdout, _ = proc.communicate()
        version = stdout.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
``` 

By using `proc.communicate()` instead of directly reading from `proc.stdout`, we ensure that the process has completed execution before retrieving its output. This should fix the bug and provide the expected output values.