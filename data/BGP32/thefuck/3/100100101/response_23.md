### Analysis
1. The `info` function is supposed to return the name and version of the current shell by running `fish -c 'echo $FISH_VERSION'` command.
2. The `test_info` test function sets up a mock for `Popen` to return the output `b'fish, version 3.5.9\n'`, but the function is looking for `fish --version` instead of `$FISH_VERSION`.
3. The bug is in the command that should be executed by `Popen` and the way the version is extracted from the output.
4. To fix the bug, the command passed to `Popen` should be `['fish', '-c', 'echo $FISH_VERSION']` instead of `['fish', '--version']`. Also, the extraction of the version from the output needs to be adjusted.

### Bug Fix
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.readline().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
``` 

By updating the command to `['fish', '-c', 'echo $FISH_VERSION']` and reading the version by `proc.stdout.readline().decode('utf-8').strip()` from the output, the function will now correctly retrieve the version information.