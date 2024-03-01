### Analysis:
- The `info` function in the `Fish` class tries to get the version of the Fish shell by running the command `echo $FISH_VERSION` using `Popen`.
- The failing test sets up the `Popen` mock to return the output `b'fish, version 3.5.9\n'` which indicates that the version should be `3.5.9`.
- However, the function is expecting to read the version using `echo $FISH_VERSION` which might not return the version in the expected format.

### Bug Cause:
- The command `echo $FISH_VERSION` is not providing the version string in the expected format for parsing by the function. This leads to the function returning an incorrect version string.

### Fix Strategy:
- Modify the command used in `Popen` to directly get the version of the Fish shell in the correct format for parsing.

### Corrected Version:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
``` 

In the corrected version, the `Popen` command is changed to `['fish', '--version']` to directly fetch the version string in a consistent format. Additionally, the `version` string is parsed to extract only the version part for uniformity.