### Explanation of the bug
The bug in the `info` function of the `Fish` class arises from how the output of the `Popen` command is being handled. The `proc.stdout.read()` method is returning a MagicMock object instead of the actual output of the `echo $FISH_VERSION` command in the Fish shell. This is causing the `version` variable to be assigned an incorrect value and leading to the function returning an incorrect result.

### Strategy to fix the bug
To fix the bug, we need to ensure that the `Popen` command is executed correctly and that we correctly retrieve the output of the command to determine the Fish shell version. We need to modify how we handle the output of the command to get the actual version information.

### Corrected version of the function
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        proc.wait()
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
``` 

In the corrected version, we first wait for the `Popen` command to finish executing before trying to read the output. Then, we read the output from `proc.stdout` after the command has completed to get the actual version information of the Fish shell.