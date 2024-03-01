The bug in the `info` function is that it is running the command `echo $FISH_VERSION` to get the Fish shell version, but in the test case, it is expecting the command `fish --version` to be executed instead. This mismatch in commands is causing the test to fail.

To fix this bug, we need to update the command being passed to `Popen` in the `info` function to be `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

With this correction, the test case provided should pass successfully as it is now aligned with the expected behavior of the `info` function.