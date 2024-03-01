### Analysis:
- The `info` function is supposed to return the name and version of the current shell.
- The function uses `Popen` to execute a command in the Fish shell and fetch the version information.
- The function then reads the output from the command and extracts the version string.
- The expected version string format is `'fish, version x.y.z'`.

### Bug:
- The bug in the `info` function is that it expects the output of the `fish -c 'echo $FISH_VERSION'` command to be in the format `'fish, version x.y.z'`, but the actual output is `'x.y.z'` without the prefix `'fish, version'`.

### Strategy for fixing the bug:
- Modify the command being executed using `Popen` to include the prefix `'fish, version '` so that the output matches the expected format.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo "fish, version $FISH_VERSION"'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().replace('fish, version ', '')
    return u'Fish Shell {}'.format(version)
``` 

Now, the corrected function should extract the version string correctly and return it in the expected format.