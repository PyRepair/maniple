### Analysis:
1. The `info` function in `fish.py` is intended to get the version of the Fish Shell by executing a command `'fish -c echo $FISH_VERSION'`.
2. The test function `test_info` in `test_fish.py` mocks the response of the subprocess call to return `'fish, version 3.5.9\n'`.
3. The issue on GitHub indicates that the usage of `thefuck -v` with Oh-My-Fish plugin causes a recursive loop because of the `info` function.
4. The current implementation in the `info` function uses the wrong command to get the version which results in a version mismatch.
5. We need to update the command and the assertion in the test function accordingly to fix this bug.

### Bug: 
The current implementation in the `info` function is trying to get the Fish Shell version using the command `'echo $FISH_VERSION'`, but it should actually use `'fish --version'`.

### Fix:
1. Modify the command in the `info` function to `'fish --version'`.
2. Update the assertion in the test function to check for the correct command `['fish', '--version']`.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

```python
def test_info(self, shell, Popen):
    Popen.return_value.stdout.read.side_effect = [b'fish, version 3.5.9\n']
    assert shell.info() == 'Fish Shell 3.5.9'
    assert Popen.call_args[0][0] == ['fish', '--version']
```