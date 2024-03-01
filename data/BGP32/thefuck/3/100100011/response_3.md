## Analysis
The `info` function in the `fish.py` file is supposed to return the name and version of the Fish shell by executing the command `fish -c 'echo $FISH_VERSION'`. However, the test provided `test_info` is expecting the command `fish --version` to be executed instead. This discrepancy between the expected command and the actual command being run in the `info` function is causing the test to fail.

## Bug Cause
The bug in the `info` function is caused by the mismatch between the command being run (`fish -c 'echo $FISH_VERSION'`) and the command expected by the test (`fish --version`). This discrepancy leads to the test failing since the output of `fish -c 'echo $FISH_VERSION'` does not match the expected output of `fish, version 3.5.9`.

## Fix Strategy
To fix the bug, we need to modify the `info` function in `fish.py` to execute the correct command `fish --version` instead of `fish -c 'echo $FISH_VERSION'`. This change will align the function with the expectations of the test and resolve the issue.

## Corrected Version
```python
# Updated fish.py with the corrected info function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

With the updated `info` function, executing `fish --version` will provide the correct version information of the Fish shell, aligning it with the expectations of the test. This fix should resolve the GitHub issue related to the mismatch in the version retrieval.