The buggy function `info` in the `Fish` class is incorrectly fetching the Fish shell version by calling `fish -c 'echo $FISH_VERSION'`, but the test is expecting the version output to be `fish, version 3.5.9\n`. The issue causing the bug is that the command used to fetch the version is incorrect and does not match the expected output of the test.

To fix the bug, we need to modify the command used to fetch the Fish shell version to match the expected output of the failing test. The correct command should be `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(' ')[2]
    return u'Fish Shell {}'.format(version)
```

This corrected version of the function will fetch the Fish shell version correctly and return the expected output for the failing test.