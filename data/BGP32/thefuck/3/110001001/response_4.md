### Explanation:
The bug in the `info` function is caused by not waiting for the process to finish before trying to read from its stdout. The call to `proc.stdout.read()` is done before the process completes, leading to incorrect or missing results.

### Strategy for Fixing the Bug:
To fix the bug, we need to ensure that the process has finished executing before trying to read from its stdout. This can be achieved by adding the `proc.wait()` method after starting the process with `Popen`.

### Corrected Version:
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        proc.wait()  # Wait for the process to finish
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
``` 

By adding `proc.wait()` after starting the process, we ensure that the function waits for the process to complete before reading from its stdout. This should fix the bug and provide the correct version of the Fish shell.