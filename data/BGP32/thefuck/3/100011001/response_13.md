### Analysis
The error message indicates that the expected output from the `info` function is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`. This suggests that the `version` variable is not correctly extracted from the output of the `Popen` command.

The issue seems to be with the way the output is read from `proc.stdout`. The `proc.stdout.read()` call from `Popen` returns a `bytes` object, and when decoding it to a string, the entire output including `'fish, version'` is being retained instead of just the version number. This causes the wrong string to be formatted in the return statement.

### Bug Fix Strategy
To fix the bug, we need to correctly decode and extract only the version number from the output of `proc.stdout.read()`.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(' ')[-1]  # Extract the last part which should be the version number
    return u'Fish Shell {}'.format(version)
``` 

This corrected version properly extracts and returns the version number from the output of `Popen` command, ensuring that the expected output matches the actual output.