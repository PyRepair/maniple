The bug in the provided function `info` is that it is trying to fetch the version of Fish shell using the command `echo $FISH_VERSION`, but the test function `test_info` is expecting the version to be extracted using the command `fish --version`. This mismatch in the expected output is causing the test to fail.

To fix the bug, we need to modify the command used to fetch the version of Fish shell to `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`.

Here is the corrected version of the buggy function `info`:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

With this correction, the function should now correctly fetch the version of Fish shell and pass the failing test provided.