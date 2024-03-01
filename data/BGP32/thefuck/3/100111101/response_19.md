### Bug Explanation
The bug in the `info` function lies in the command passed to the `Popen` function. The current command `['fish', '-c', 'echo $FISH_VERSION']` does not retrieve the version number directly, resulting in the incorrect version string `'fish, version 3.5.9'` being returned instead of just `'3.5.9'`.

### Fix Strategy
To fix the bug, we need to change the command passed to `Popen` to retrieve only the version string without any additional text.

### The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    # extract version number only
    version = version.split()[-1]
    return u'Fish Shell {}'.format(version)
``` 

By correcting the command to `['fish', '--version']`, we ensure that only the version number is returned, which matches the expected output `'Fish Shell 3.5.9'`.
