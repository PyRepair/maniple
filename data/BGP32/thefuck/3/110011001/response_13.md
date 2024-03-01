### Analysis
- The `info` function in the `Fish` class is supposed to return the name and version of the current shell by running a command in the Fish shell.
- The error message indicates that the actual output from the `info` function is not matching the expected output.
- The `Popen` mock object is being used to simulate running a command in the Fish shell.

### Bug
The bug in the code is caused by the `echo $FISH_VERSION` command returning both the name of the shell and the version, which is not handled correctly in the `info` function.

### Fix
To fix the bug, we need to extract only the version number from the output of the `echo $FISH_VERSION` command.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split(', version ')[1]
        return u'Fish Shell {}'.format(version)
```

With this correction, the `info` function will extract only the version number from the output of the command and return it as 'Fish Shell <version>'. This should make the test pass successfully.