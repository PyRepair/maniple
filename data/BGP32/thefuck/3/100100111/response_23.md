### Analysis
- The function `info` is supposed to return the version of the Fish Shell by executing a command using `Popen`.
- The test case `test_info` mocks the `Popen` function to return a specific output when called with `['fish', '-c', 'echo $FISH_VERSION']`.
- The test case expects the function to return `Fish Shell 3.5.9` and also checks the command passed to `Popen`.

### Error Location
The issue lies in the way the version is being extracted from the output of the `Popen` command.

### Cause of the Bug
The command being passed to `Popen` in the function is `['fish', '-c', 'echo $FISH_VERSION']`, but the test case expects `['fish', '--version']`. Additionally, the extraction of the version from the output is incorrect.

### Strategy for Fixing the Bug
1. Update the command passed to `Popen` to `['fish', '--version']` to match the test case expectation.
2. Correctly read and extract the version from the output of the `Popen` command.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').split(' ')[2].strip()
    return u'Fish Shell {}'.format(version)
``` 

This corrected version of the function should now pass the failing test case and provide the expected output.