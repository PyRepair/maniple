The bug in the `info` function stems from the fact that the command used to fetch the Fish shell version is incorrect. The command `'echo $FISH_VERSION'` does not provide the version number in the correct format. Moreover, the test case is expecting the output of the command `'fish --version'`, which provides the correct version information.

### Bug Explanation:
- The function is currently running the command `'echo $FISH_VERSION'`, which does not give the version number directly.
- The test case is expecting the output of the correct command `'fish --version'`.

### Bug Fix Strategy:
1. Update the command in `Popen` to `['fish', '--version']` to retrieve the correct version information.
2. Modify the assertion in the test case to check for the correct command execution.


### Corrected Version:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

### Test Case (Updated Assertion):
```python
def test_info(self, shell, Popen):
    Popen.return_value.stdout.read.side_effect = [b'fish, version 3.5.9\n']
    assert shell.info() == 'Fish Shell 3.5.9'
    assert Popen.call_args[0][0] == ['fish', '--version']
```