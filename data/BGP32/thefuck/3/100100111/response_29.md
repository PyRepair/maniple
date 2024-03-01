## Analysis:
1. The `info` function within `shells/fish.py` is trying to get the version of Fish shell by running the command `echo $FISH_VERSION` and extracting the version from the output.
2. The test case in `test_fish.py` sets up the mocking behavior for `stdout.read` to return `b'fish, version 3.5.9\n'` when `Popen` is called with `['fish', '--version']`.
3. The current implementation of the `info` function is incorrect because it is not using `['fish', '--version']` to get the shell version, leading to a mismatch between the expected and actual output.
4. The bug is caused by the incorrect command used to retrieve the Fish shell version inside the `info` function.
5. To fix the bug, the command passed to `Popen` should be changed to `['fish', '--version']` instead of `echo $FISH_VERSION`.

## Bug Fix:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

By updating the command to `['fish', '--version']` in the `info` function, the correct version output can be obtained, which should resolve the issue and make the function pass the failing test case.