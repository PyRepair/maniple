### Analysis:
1. The `info` function in `fish.py` is attempting to retrieve the version of the Fish shell by running `fish -c 'echo $FISH_VERSION'`. However, in the failing test, it is asserting against the version output of `fish --version`.
2. The issue reported on GitHub states that there is a recursive loop triggered by using `thefuck -v` with the Oh-My-Fish plugin due to this discrepancy in version retrieval.

### Bug Cause:
The bug is caused by the mismatch between the command used to retrieve the Fish shell version in the `info` function (`fish -c 'echo $FISH_VERSION'`) and the expected version output in the failing test (`fish --version`). This discrepancy leads to incorrect version comparison and potentially triggers recursive loops as reported on GitHub.

### Fix Strategy:
1. Modify the `info` function to execute `fish --version` command to fetch the version string that matches the expected version output in the failing test.
2. Update the test to reflect the correct expected version string obtained from `fish --version`.
3. Ensure that the function returns the correct format with the obtained version.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(', ')[1])
```

With this corrected version, the `info` function will fetch the Fish shell version correctly using the `fish --version` command, and the output will be parsed to extract only the version number for comparison in the test.

Update the failing test as follows:
```python
def test_info(self, shell, Popen):
    Popen.return_value.stdout.read.side_effect = [b'fish, version 3.5.9\n']
    assert shell.info() == 'Fish Shell 3.5.9'
    assert Popen.call_args[0][0] == ['fish', '--version']
```

This corrected version should address the discrepancy, pass the failing test, and resolve the reported GitHub issue.