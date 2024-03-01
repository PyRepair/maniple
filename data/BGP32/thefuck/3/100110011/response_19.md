## Analysis:
1. The `info` function in the `fish.py` file is not correctly fetching the Fish shell version. It is using the wrong command to get the version, which leads to a mismatch in the expected output in the test.
2. The test function `test_info` expects the `shell.info()` to return 'Fish Shell 3.5.9', but due to the incorrect command used in the `info` function, the actual output is 'Fish Shell fish, version 3.5.9'.

## Bug Cause:
The bug occurs due to the incorrect command 'echo $FISH_VERSION' used to get the Fish shell version in the `info` function. This results in the actual shell info being in the format 'fish, version 3.5.9' instead of just the version number '3.5.9'. As a result, the test fails due to the mismatch in the expected and actual output.

## Fix Strategy:
To fix the bug, we need to change the command used to retrieve the Fish shell version. Instead of 'echo $FISH_VERSION', we should use 'fish --version' to get the correct version information.

## Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').split()[-1]
    return u'Fish Shell {}'.format(version)
```

By making this change, the `info` function will correctly extract just the version number from the shell command output and match the expected output in the test.