## Analysis:
1. The buggy function `info` in `shells/fish.py` is using the command `fish -c 'echo $FISH_VERSION'` to retrieve the version of the Fish shell. 
2. The test function `test_info` in `tests/shells/test_fish.py` is mocking the `Popen` object and setting the return value of `stdout.read` to `b'fish, version 3.5.9\n'`.
3. The bug is causing the test to fail as the expected version `'Fish Shell 3.5.9'` is not being correctly parsed from the output of `Popen`.
4. The issue on GitHub highlights that the use of `-v` in `thefuck` with Oh-My-Fish plugin triggers a recursive loop due to this exact bug in `shells/fish.py`.
   
## Bug Cause:
The bug is due to the discrepancy between the command used to retrieve the version (`echo $FISH_VERSION`) and the expected output in the test (`'fish, version 3.5.9\n'`). Additionally, the call_args in the test is not matching the command used in the `Popen`.

## Fix Strategy:
To fix the bug, we need to update the command executed by `Popen` to actually get the version of Fish shell. Additionally, we should update the test to match the new command being executed and the expected output.

## Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version_number = version.split(', ')[1].split(' ')[1]
    return u'Fish Shell {}'.format(version_number)
```

In this corrected version, the `Popen` command is updated to use `['fish', '--version']` to get the correct version. Additionally, the parsing of the version from the output is adjusted to match the format of `fish --version`.