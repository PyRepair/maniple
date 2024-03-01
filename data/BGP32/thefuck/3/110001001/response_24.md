### Explanation of the bug
The bug in the `info` function is caused by the incorrect handling of the `Popen` object and its stdout. The function creates a `Popen` object to execute a command to get the Fish shell version, but does not properly handle reading the output from the process. This results in the `version` variable containing the command itself (`fish, version 3.5.9`) instead of just the version number.

### Bug fix strategy
To fix the bug, we need to properly read the output from the `Popen` process to extract only the version number. We can use the `communicate` method of the `Popen` object to read both stdout and stderr streams of the process. This approach ensures that the function correctly captures the intended output.

### Corrected version of the function
```python
# The relative path of the buggy file: thefuck/shells/fish.py

# The declaration of the class containing the fixed function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        out, _ = proc.communicate()
        version = out.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
``` 

In the corrected version, we use `proc.communicate()` to read the stdout stream of the process and ignore the stderr. This ensures that we correctly extract the Fish shell version number from the command output.