### Explanation:
The bug in the `info` function is caused by the incorrect command used to retrieve the Fish shell version. The function is currently using `"echo $FISH_VERSION"` as the command to get the version, but in the failing test, the expected version output is `"fish, version 3.5.9"`.

### Strategy for fixing the bug:
1. Update the command passed to `Popen` to match the expected output format from the failing test.
2. Strip the unnecessary characters and extract the version number correctly.

### Corrected version of the buggy function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(', version ')[-1]
    return u'Fish Shell {}'.format(version)
``` 

After applying these changes, re-run the failing test to ensure that the corrected function passes successfully.