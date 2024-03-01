## Analysis
1. The `info` function in the `fish.py` file is attempting to retrieve the version of the Fish shell by executing `echo $FISH_VERSION`.
2. The failing test in `test_fish.py` provides the expected output as `'Fish Shell 3.5.9'` and the expected command as `['fish', '--version']`.
3. The bug causes the function to use the wrong command to retrieve the version, leading to incorrect output.
4. To fix the bug, the function should execute `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`.

## Bug Fix
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

By changing the command to `['fish', '--version']`, the function will correctly retrieve the version of the Fish shell. Additionally, extracting the actual version number by splitting the output and selecting the last element will ensure the function returns the expected output.