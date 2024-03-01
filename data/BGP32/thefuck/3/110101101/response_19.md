The bug in the `info` function is due to the incorrect command used to retrieve the Fish shell version. The command `echo $FISH_VERSION` is not valid for retrieving the shell version. Instead, we should use the `--version` flag with the `fish` command.

### Strategy for fixing the bug:
1. Update the command in `Popen` to `['fish', '--version']` to correctly retrieve the Fish shell version.
2. Strip the unnecessary text and formatting from the output to get just the version number.

### Corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

By making the above changes, the `info` function should now correctly retrieve and format the Fish shell version, passing the failing test case provided.