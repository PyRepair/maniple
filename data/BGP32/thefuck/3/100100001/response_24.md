The bug in the `info` function arises from the incorrect command used to retrieve the Fish shell version in the `Popen` call. The test code expects the version to be obtained using `fish --version`, but the buggy function is using `echo $FISH_VERSION`.

To fix the bug, we need to update the `Popen` call in the `info` function to use `fish --version` instead. Additionally, the decoding method for the output should be adjusted accordingly.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').split()[2].strip()
    return u'Fish Shell {}'.format(version)
```

With this correction, the `info` function will correctly extract the version number using `fish --version` and decode the output to obtain the required version information. This corrected version should pass the failing test.