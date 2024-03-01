## Identification of Bugs:
1. The `info` function is trying to retrieve the Fish shell version using `echo $FISH_VERSION`, but in the failing test function `test_info`, the expected command is `fish --version`.
2. The `info` function incorrectly reads the output from the command via `proc.stdout.read().decode('utf-8').strip()`, which may cause inconsistencies.

## Bug Causes:
The main cause of the bug is the mismatch between the command used to retrieve the Fish shell version in the `info` function and the expected command in the failing test `test_info`. Additionally, the way the function reads the output may not handle the provided output format correctly.

## Bug Fix Strategy:
1. Update the command used in the `info` function to `['fish', '--version']` to match the expected output in the failing test.
2. Modify how the function reads and decodes the output to ensure compatibility with the provided output format.

## The Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return 'Fish Shell {}'.format(version)
```

With the corrected version of the function, it should now correctly retrieve the Fish shell version by executing `fish --version` and then extract the version number from the output. This version of the function should pass the failing test `test_info` and address the issue reported on GitHub.