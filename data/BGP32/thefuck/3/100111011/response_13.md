### Analysis
The buggy function `info` in the `Fish` class is supposed to return the name and version of the Fish shell. However, the command being executed in the `Popen` call `['fish', '-c', 'echo $FISH_VERSION']` is not consistent with what is being checked in the failing test `['fish', '--version']`.

### Error Cause
1. The `info` function is expecting the output from `echo $FISH_VERSION`, but the failing test is providing output that includes 'version' and specific version numbers.
2. The differing output formats lead to a failed assertion error when comparing the expected version 'Fish Shell 3.5.9' with the version extracted from the output 'Fish Shell fish, version 3.5.9'.

### Fix Strategy
To fix the bug:
1. Update the command executed in the `Popen` call to `['fish', '--version']` to retrieve the correct version information.
2. Extract and format the version information accordingly to match the expected output.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

With this corrected version, the `info` function in the `Fish` class will extract the correct version information from the Fish shell and format it as 'Fish Shell version_number', resolving the assertion error in the failing test.