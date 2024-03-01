### Analysis:
- The error message shows that the `info` function is returning the wrong version string. Instead of `'Fish Shell 3.5.9'`, it is returning `'Fish Shell fish, version 3.5.9'`.
- The bug is caused by the `echo $FISH_VERSION` command in the `Popen` call, which is returning the version string along with some additional text.
- The `strip()` method is not removing all unnecessary characters from the version string.

### Fix:
- Modify the `version = proc.stdout.read().decode('utf-8').strip()` line to extract only the version number.
- Update the `Fish Shell {}` format string to include the correct version number.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(", version ")[1]
    return u'Fish Shell {}'.format(version)
```