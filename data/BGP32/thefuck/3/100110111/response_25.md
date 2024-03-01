## Analysis
1. The `info` function in `shells/fish.py` is reading the Fish shell version by executing `fish -c 'echo $FISH_VERSION'`. However, in the test, the expected output is `'Fish Shell 3.5.9'` which means the version format is different.
2. The error message indicates that the actual output includes additional text (`'fish, version 3.5.9'`) compared to the expected output (`'3.5.9'`).
3. The test function expects the command `['fish', '--version']` to be executed, but the actual command being executed is `['fish', '-c', 'echo $FISH_VERSION']`.
4. The GitHub issue suggests that there was a problem related to using `-v` with TheFuck plugin and Oh-My-Fish, which indicates a potential issue with shell initialization.

## Bug Cause
The bug is caused by the mismatch in the expected output format and the actual output format from the `info` function. Additionally, the incorrect command (`['fish', '-c', 'echo $FISH_VERSION']` instead of `['fish', '--version']`) is being used to retrieve the version.

## Fix Strategy
To fix the bug, we need to:
- Modify the command executed in the `info` function to `['fish', '--version']` to align with the test expectation.
- Extract the version number from the output correctly to match the expected format.
- Update the `info` function to return the expected output format.

## Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.readline().decode('utf-8').split()[2]
    return u'Fish Shell {}'.format(version)
```

With the corrected version, the `info` function should correctly read the Fish shell version and return it in the expected format, resolving the bug.