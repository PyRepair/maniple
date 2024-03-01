### Analysis
The buggy function `info` is trying to retrieve the version of the Fish shell by running a command `echo $FISH_VERSION`. However, in the failing test, the expected version is `'Fish Shell 3.5.9'` whereas the buggy function is returning the version in a different format `'Fish Shell fish, version 3.5.9'`. This discrepancy is causing the assertion error.

The bug is mainly due to the incorrect command used to get the Fish shell version and the incorrect formatting in the return statement.

### Bug Fix Strategy
1. Change the command in the `Popen` call to `['fish', '--version']` to correctly retrieve the version.
2. Update the formatting of the return statement to match the expected format `'Fish Shell <version>'`.

### Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(', version ')[1])
```