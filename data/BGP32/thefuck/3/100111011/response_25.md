After analyzing the provided information, it appears that the bug in the `info` function of the `Fish` class is due to two main reasons:
1. The command used to retrieve the Fish shell version is incorrect. The current command `['fish', '-c', 'echo $FISH_VERSION']` should be `['fish', '--version']`.
2. The comparison in the test function is expecting the string `'Fish Shell 3.5.9'`, but the retrieved version includes additional text ("fish, version").

To fix the bug, we need to update the command used to retrieve the Fish shell version and ensure the comparison in the test function matches the expected output.

Here is the corrected version of the `info` function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].strip().split(' ')[1]  # Extract the version number
    return u'Fish Shell {}'.format(version)
```

With this correction, the `info` function will properly extract the version number from the output of the `fish --version` command.

Additionally, the test function needs to be updated to reflect the corrected output. Here is the updated test function:
```python
def test_info(self, shell, Popen):
    Popen.return_value.stdout.read.side_effect = [b'fish, version 3.5.9\n']
    assert shell.info() == 'Fish Shell 3.5.9'
    assert Popen.call_args[0][0] == ['fish', '--version']
```

By making these changes, the `info` function should now correctly retrieve and format the Fish shell version, and the test function should pass without any assertion errors.