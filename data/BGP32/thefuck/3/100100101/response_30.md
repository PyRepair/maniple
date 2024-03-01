### Analysis
1. The buggy function `info` uses the command `echo $FISH_VERSION` to get the fish shell version. However, in the failing test, the expected output is `'fish, version 3.5.9\n'` which means that the command should be changed to `fish --version`.
2. The `Popen` call in the `info` function is not using the correct arguments, it should be `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`.

### Bug Cause
The bug is caused by the incorrect command `echo $FISH_VERSION` in the `info` function, leading to the incorrect version output. Additionally, the `Popen` call uses the wrong arguments, resulting in a mismatch with the expected output in the failing test.

### Strategy for Bug Fix
1. Modify the command in the `Popen` call to use `['fish', '--version']`.
2. Update the test case to reflect the correct expected version output based on the modified command.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]
    return u'Fish Shell {}'.format(version)

```

The corrected function now uses the correct command `['fish', '--version']` to get the fish shell version. Additionally, it extracts and formats the version properly based on the expected output from the failing test.