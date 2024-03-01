### Analysis
- The `info` function is trying to retrieve the version of the Fish shell by running the command `echo $FISH_VERSION` in a subprocess.
- It then reads the output from the subprocess, decodes it, and formats it into a string.
- The issue might be related to how the output is being read from the subprocess.

### Bug
The bug likely lies in how the stdout from the subprocess is being read. The code is currently using `proc.stdout.read().decode('utf-8').strip()` to read the output, but this approach may not work reliably.

### Fix
To fix the bug, we can change how the output is read from the subprocess. Instead of using `proc.stdout.read().decode('utf-8').strip()`, we can use `communicate()` method of the subprocess to read the output. This method ensures that all data is read from the pipe and also handles the decoding in a more reliable way.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output, _ = proc.communicate()
        version = output.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```