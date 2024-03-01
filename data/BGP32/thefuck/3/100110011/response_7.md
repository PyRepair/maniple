### Analysis:
1. The `info` function in the `fish.py` file is attempting to retrieve the version of Fish Shell by running the command `fish -c 'echo $FISH_VERSION'`, but the test code expects it to run `fish --version`.
2. The `Popen` call is using `['fish', '-c', 'echo $FISH_VERSION']` instead of `['fish', '--version']`.
3. The failing test and the error message clearly indicate that the version output is not being parsed correctly in the `info` function, resulting in a mismatch in the output string comparison.
4. To fix the bug, the `Popen` call should be updated to use `['fish', '--version']` to correctly fetch the version number.

### Bug Fix:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```

### Updated Test Function:
```python
def test_info(self, shell, Popen):
    Popen.return_value.stdout.read.side_effect = [b'fish, version 3.5.9\n']
    assert shell.info() == 'Fish Shell 3.5.9'
    assert Popen.call_args[0][0] == ['fish', '--version']
```

By making this change, the `info` function will correctly fetch the version of Fish Shell using the `fish --version` command and parse the output to return the correct version number.