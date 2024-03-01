### Bug Explanation
The bug in the `info` function is caused by two main issues:
1. The command used to get the Fish shell version is incorrect. The command should be `fish --version` instead of `echo $FISH_VERSION`.
2. The test function `test_info` is expecting the command to be `fish --version`, but the function is using `echo $FISH_VERSION`.

### Bug Fix Strategy
To fix the bug, we need to update the command to get the Fish shell version to `fish --version` and modify the test function to expect this command.

### Corrected Version of the `info` Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

### Updated Test Function
```python
    def test_info(self, shell, Popen):
        Popen.return_value.stdout.read.return_value = b'fish, version 3.5.9\n'
        assert shell.info() == 'Fish Shell 3.5.9'
        assert Popen.call_args[0][0] == ['fish', '--version']
``` 

After applying these changes, running the failing test should now pass with the corrected function.