### Explanation
The bug in the `info` function is that it attempts to read the output from the `proc.stdout` using `read()` method, which is not the correct way to read the output from a subprocess in Python. 

### Strategy for fixing the bug
To fix this bug, we need to use the `communicate()` method of the `proc` object, which will read the output from the subprocess correctly.

### Corrected version of the function
```python
# The relative path of the corrected file: thefuck/shells/fish.py

class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output, _ = proc.communicate()
        version = output.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
``` 

By using the `proc.communicate()` method to read the output from the subprocess, we ensure that the function correctly retrieves the version of the Fish shell and returns it in the desired format.