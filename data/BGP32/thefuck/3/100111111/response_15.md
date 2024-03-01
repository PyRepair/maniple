## Bug Fix Strategy
1. The bug seems to be caused by the incorrect command used to retrieve the Fish shell version, leading to an extra 'fish,' text in the version.
2. To fix this bug, we should modify the command to retrieve the correct version information without any extra characters.

## The corrected version of the buggy function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]  # Extracting only the version number
    return u'Fish Shell {}'.format(version)
```

By modifying the command to use `--version` instead of `echo $FISH_VERSION`, we can ensure that only the version number is captured without any extra characters. This should address the bug and make the function return the correct version of the Fish shell when called.