The bug in the `info` function is related to the incorrect command being used to retrieve the Fish shell version. In the function, the command being executed is `fish -c 'echo $FISH_VERSION'`, which is trying to directly print the value of the `FISH_VERSION` environment variable. However, this is not the correct way to retrieve the Fish shell version.

To fix this bug, we need to change the command to `fish --version` to accurately fetch the version number that matches the expected value in the test.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(", ")[1].strip()
    return u'Fish Shell {}'.format(version)
```

With this fix, the command used to retrieve the Fish shell version will be correct. This should make the `info` function return the expected output 'Fish Shell 3.5.9'.