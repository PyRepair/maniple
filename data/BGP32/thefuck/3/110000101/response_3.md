### Analysis
1. The function `info()` is trying to get the version of the Fish shell by running a command using `Popen`.
2. The potential error lies in how the function is reading the output from the `Popen` process.
3. The bug is caused because the function is trying to read the output from `proc.stdout` before the process has finished running and writing the output. This results in an empty string being returned.
4. To fix the bug, we need to wait for the process to finish running and then read the output from `proc.stdout` correctly.

### Correction
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        out, _ = proc.communicate()
        version = out.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
``` 

By using `proc.communicate()` instead of directly calling `proc.stdout.read()`, we ensure that the process finishes running and then read the output correctly.