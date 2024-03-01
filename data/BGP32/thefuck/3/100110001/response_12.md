### Analysis:
- The `info` function in the `Fish` class of the `thefuck` package is attempting to get the version of the Fish shell by executing a command.
- The expected output in the failing test is `'Fish Shell 3.5.9'`, but the actual output contains an additional prefix `fish,` which causes the assertion error.
- The function is trying to get the Fish shell version by executing the command `echo $FISH_VERSION`.

### Issue:
- The command used in the `info` function does not match the expected command in the failing test. The command should be modified to `echo $version` in order to align with the test expectation.

### Strategy for fixing the bug:
- Change the command in the Popen call to `['fish', '-c', 'echo $version']` to correctly get the Fish shell version.
- Update the function to strip the unnecessary prefix `fish,` from the version output.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()  # Read output and decode from bytes
    version = output.replace('fish, version ', '')  # Remove prefix 'fish, version'
    return u'Fish Shell {}'.format(version)
``` 

With this correction, the function will correctly extract the Fish shell version and return it without any unnecessary prefixes, matching the expected output in the failing test.