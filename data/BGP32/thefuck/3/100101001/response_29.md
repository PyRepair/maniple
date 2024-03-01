### Explanation
The bug in the `info` function lies in the command used to retrieve the Fish shell version. The command `echo $FISH_VERSION` does not actually fetch the version number; instead, it prints the literal string `$FISH_VERSION`. This causes the version variable to be incorrect.

### Strategy for fixing the bug
To fix the bug, we need to modify the command so that it correctly retrieves the Fish shell version. One way to do this is to change the command to `fish --version`, which will output the version information.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
``` 

With this modification, the function will now correctly retrieve the Fish shell version and pass the failing test.