The issue with the current `info` function in the `fish.py` file is that it is trying to read the version of Fish shell using the command `echo $FISH_VERSION` in a separate process, but the test is expecting the version to be fetched using the `fish --version` command.

To fix this issue, we need to change the command used in the `Popen` call to `['fish', '--version']` and then parse the output to extract the version number.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version_str = proc.stdout.read().decode('utf-8').strip()
    version = version_str.split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

By updating the command to `['fish', '--version']` and extracting the version number correctly from the output, the corrected `info` function should now pass the failing test.