### Steps to fix the bug:
1. The current implementation of the `info` function is not correctly extracting the version of the Fish shell. The `echo` command used in the subprocess call is returning the output as `'fish, version 3.5.9\n'` instead of just the version number.
2. The `decode('utf-8').strip()` method is removing any whitespace characters from the beginning and end of the string but is not filtering out the unnecessary text before the version number.
3. The `u'Fish Shell {}'.format(version)` line then adds the unnecessary text before the version number, leading to the failed assertion in the test.
4. To fix this bug, we need to modify the subprocess call to only return the version number by using a command like `'echo $FISH_VERSION | cut -d" " -f3'`.

### Corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION | cut -d" " -f3'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By changing the subprocess command to extract only the version number using `cut -d" " -f3`, we ensure that the version extracted is just the number without any additional text. This change should make the function return the correct version and pass the failing test.