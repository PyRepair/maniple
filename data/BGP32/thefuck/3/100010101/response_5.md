### Analysis
1. The error message indicates that the function is returning a string with an unexpected format `'Fish Shell fish, version 3.5.9'` instead of the expected format `'Fish Shell 3.5.9'`.
2. The issue lies in the line `version = proc.stdout.read().decode('utf-8').strip()`. It seems that the process output `'fish, version 3.5.9\n'` is not being parsed correctly.
3. The `decode('utf-8').strip()` method is not correctly handling the output to extract just the version number.
4. To fix the bug, we need to modify the code that processes the output of the `Popen` command to correctly extract the version number.

### Bug Fix
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').split(',')[1].split()[1].strip()
    return u'Fish Shell {}'.format(version)
```

By using the `split()` method with `','` as the delimiter to extract the second part after the comma, and then `split()` with a space as the delimiter to get just the version number, the bug should be fixed.

This fix should correctly extract the version number and return it in the expected format.