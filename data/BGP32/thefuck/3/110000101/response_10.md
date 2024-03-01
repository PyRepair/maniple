### Analysis
1. The function `info` in the `Fish` class is attempting to retrieve the version of the Fish shell by executing a command.
2. The function uses `Popen` to execute a command and retrieve the output.
3. The issue lies in how the function is trying to read the output from the process.
4. Currently, the function is trying to directly read from `proc.stdout`, which may not be the correct way to get the output.

### Bug
The bug lies in the way the function is attempting to read the output from the process. It is trying to directly read `proc.stdout`, which may not provide the complete output.

### Fix
To fix the bug, we should use the `communicate()` method of the process to properly read the output.

### Corrected Version
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