## Explanation
The bug in the `info` function of the Fish shell script is due to the fact that the command being executed (`echo $FISH_VERSION`) does not match the expected output format (`'Fish, version x.x'`). This discrepancy causes the assertion to fail because the version number retrieved from the command output includes unnecessary text.

## Fix Strategy
To fix the bug, the command being executed by `Popen` needs to be changed to retrieve only the version number without any additional text. This can be achieved by running the command `fish --version` instead of `echo $FISH_VERSION`.

## Corrected Function
Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version_info = proc.stdout.read().decode('utf-8').strip()
    version = version_info.split()[2]
    return u'Fish Shell {}'.format(version)
```

By changing the command to `['fish', '--version']` and extracting the version number correctly from the output, the function should now return the expected result.