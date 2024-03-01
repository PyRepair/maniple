## Bug Analysis:
- The `info` function in the `fish.py` file is intended to return the version of the Fish shell.
- The current implementation of the `info` function uses `echo $FISH_VERSION` command to retrieve the version, which is incorrect.
- The test is trying to read the version from `fish, version 3.5.9\n`, but the function is reading `FISH_VERSION` environment variable.
- The issue on GitHub suggests that calling `thefuck -v` triggers a recursive loop due to this incorrect implementation.

## Bug Cause:
- The `info` function is fetching the version by running the command `echo $FISH_VERSION`, but it should actually run `fish --version` to get the version string.
- Due to this incorrect command, the test is set up to expect a different version string, leading to test failure and potential recursive loops as mentioned in the GitHub issue.

## Bug Fix Strategy:
- Revise the command in the `Popen` call in the `info` function to execute `fish --version` instead of `echo $FISH_VERSION`.
- Modify the test data to match the output of `fish --version`.
- Update the assertion in the test to match the correct command used in the `info` function.

## Corrected Version:
```python
# Updated and corrected `info` function in fish.py

def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(' ')[2]
    return u'Fish Shell {}'.format(version)
```

With the corrected version above, the function should now correctly fetch the Fish shell version.
Adjust the test data accordingly:
```python
# Updated test_fish.py

def test_info(self, shell, Popen):
    Popen.return_value.stdout.read.side_effect = [b'fish, version 3.5.9\n']
    assert shell.info() == 'Fish Shell 3.5.9'
    assert Popen.call_args[0][0] == ['fish', '--version']
```

This corrected version should resolve the bug reported in the GitHub issue and prevent recursive loops due to incorrect version retrieval.