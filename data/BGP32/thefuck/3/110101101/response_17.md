The bug in the `info` function is that the command being executed to get the Fish shell version is incorrect. The command should be `fish --version` instead of `echo $FISH_VERSION`.

### Bug Explanation:
- The `test_info` function provides the expected output `'fish, version 3.5.9\n'` for the `Popen` to read, indicating that the shell version is being obtained by running the command `fish, version 3.5.9\n`.
- However, in the `info` function, the command used is `echo $FISH_VERSION`, which will not provide the actual version of the shell.
- This discrepancy leads to the failing test since the output of `echo $FISH_VERSION` does not match the expected version string.

### Fix Strategy:
- Modify the command being executed by `Popen` in the `info` function to `fish --version` to accurately obtain the Fish shell version.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```