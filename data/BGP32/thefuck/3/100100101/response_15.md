### Bug Analysis
The buggy function `info` is supposed to retrieve the version of the Fish shell by running the command `echo $FISH_VERSION` using the `Popen` function. The bug seems to be caused by the incorrect command being passed to `Popen` and the way the output is read and processed.

### Bug Explanation
1. The command passed to `Popen` to fetch the Fish shell version is incorrect. It should be `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`.
2. The function should read the version output from `proc.stdout` instead of using `proc.stdout.read().decode('utf-8').strip()`.

### Bug Fix Strategy
1. Update the command passed to `Popen` to fetch the Fish shell version correctly.
2. Read the version value directly from `proc.stdout` instead of reading and decoding it separately.

### The corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.readline().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```