### Analysis:
The bug in the `info` function is caused by fetching the shell version by running the command `echo $FISH_VERSION` instead of `fish --version`. This leads to an incorrect version format being returned.

### Bug:
The `info` function is expecting the output of `fish --version` in the format `3.5.9`, but it receives `fish, version 3.5.9` instead.

### Fix:
Modify the command in Popen to `['fish', '--version']` to correctly fetch the version of Fish shell.

### Corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split()[-1]  # Extract only the version number
    return u'Fish Shell {}'.format(version)
```