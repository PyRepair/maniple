### Analysis
1. The `info` function is supposed to retrieve the version of the Fish shell by executing a command and reading its output.
2. The test function sets the expected output version to `'3.5.9'` but the command executed is `'echo $FISH_VERSION'` which does not return the version in the expected format.
3. The bug is caused by the incorrect command used to retrieve the version of the Fish shell.
4. To fix the bug, the command needs to be changed to `'fish --version'` to correctly obtain the version of the Fish shell.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```