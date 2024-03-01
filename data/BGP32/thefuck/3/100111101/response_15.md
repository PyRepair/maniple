The bug in the `info` function is caused by the incorrect command used to retrieve the Fish shell version. The command `echo $FISH_VERSION` does not provide the correct version format and includes unnecessary text. 

To fix the bug, we need to change the command to `fish --version` to correctly retrieve the version information.

Here is the corrected version of the function:

```python
# The relative path of the corrected file: thefuck/shells/fish.py

def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', ')[-1]
    return u'Fish Shell {}'.format(version)
```

This corrected version should now correctly retrieve the Fish shell version and pass the failing test, satisfying the expected input/output values.