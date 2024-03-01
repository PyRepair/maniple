### Bug Explanation:
The bug in the `info` function lies in the command used to retrieve the version of the Fish shell. The command `echo $FISH_VERSION` is returning the string `'fish, version 3.5.9'` instead of just the version number `3.5.9`, which causes the assertion to fail since the expected output is `'Fish Shell 3.5.9'`.

### Bug Fix:
To fix the bug, we need to update the command in the `Popen` call to `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`. This will directly return the version number of the Fish shell.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].strip()  # Extracting only the version number
    return u'Fish Shell {}'.format(version)
```