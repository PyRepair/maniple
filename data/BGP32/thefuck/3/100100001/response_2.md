The bug in the `info` function of the `fish.py` file is that it is trying to read the version of Fish Shell by executing `echo $FISH_VERSION` command, but in the failing test, it expects the version to be obtained by executing `fish --version` command.

To fix this bug, we need to update the command used to retrieve the version of Fish Shell in the `info` function from `echo $FISH_VERSION` to `fish --version`.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split()[-1])
```

After making this change, the `info` function in the `fish.py` file should now correctly retrieve the version of Fish Shell when tested with the failing test.