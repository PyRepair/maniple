The bug in the `info` function is caused by the incorrect command used to retrieve the Fish shell version. The function is currently using `echo $FISH_VERSION` which outputs the version as `'fish, version 3.5.9'`, including unnecessary text. The `info` function should only extract the version number without any additional text.

To fix the bug, we need to update the command used to retrieve the version. We should use `fish --version` instead of `echo $FISH_VERSION`.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

With this fix, the function should now correctly extract the version number without any additional text and pass the failing test.

Please rerun the failing test to confirm the bug fix.