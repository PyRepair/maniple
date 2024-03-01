### Identified Bug:
The bug in the `info` function of the `Fish` shell class is that it is using the command `echo $FISH_VERSION` to extract the version of Fish shell, but in the failing test, the expected version format is different (`'Fish Shell 3.5.9'`). Additionally, the `Popen` call should be using the `--version` flag instead of `echo $FISH_VERSION`. This mismatch causes the assertion error since the extracted version is not in the expected format.

### Suggested Fix:
1. Update the `Popen` call to use `['fish', '--version']` to get the shell version.
2. Modify the extraction process to parse the version string appropriately to match the expected format.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(', ')[1]
    return u'Fish Shell {}'.format(version)
``` 

With this correction, the function will extract the version correctly and present it in the expected format, resolving the failing test.