The bug in the provided function `info` arises from the fact that the command used to retrieve the Fish shell version should be `'fish --version'` instead of `'echo $FISH_VERSION'`. This incorrect command results in the version not being fetched correctly, leading to the failing test.

To fix the bug, the command used in the `Popen` call should be updated to `'fish --version'` to correctly retrieve the Fish shell version.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return 'Fish Shell {}'.format(version)
```

With this correction, the function should now extract the Fish shell version correctly and pass the failing test.