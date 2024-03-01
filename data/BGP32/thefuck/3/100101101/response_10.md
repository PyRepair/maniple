## Fixing the Bug

### Bug Analysis
The `info` function in the `fish.py` file is attempting to retrieve the version of the Fish shell by executing the command `echo $FISH_VERSION`. However, in the failing test, the expected version does not match the actual version extracted from the command output. This discrepancy is causing the test to fail.

### Bug Fix Strategy
To fix this bug, we need to modify the command executed to retrieve the Fish shell version so that it matches the expected format `'Fish Shell <version>'`.

### Corrected Version

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split()[-1]  # Extracting only the version number
    return u'Fish Shell {}'.format(version)
```

The corrected version modifies the command passed to `Popen` to `['fish', '--version']`, which will directly provide the version string. The extracted version is then properly formatted and returned as `'Fish Shell <version>'`. This should now pass the failing test.