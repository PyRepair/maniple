## Bug Fix Strategy
The bug in the `info` method of the `Fish` class is due to the fact that the command used to get the version of Fish shell is incorrect. The correct command should be `fish --version` instead of `echo $FISH_VERSION`.

To fix this bug, we need to modify the command passed to `Popen` to execute `fish --version` instead. This will ensure that the version retrieved is correct and matches the expected output in the failing test.

## Corrected Version of the `info` Method
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By updating the command to `fish --version`, the function will now correctly retrieve the Fish shell version and the failing test should pass as expected.