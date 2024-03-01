### Bug Explanation
The bug in the `info()` function lies in the command used to retrieve the Fish shell version. The command `echo $FISH_VERSION` does not output the version of the Fish shell directly, but rather a string containing "fish, version X.X.X". This causes the assertion in the test to fail as it expects only the version number. Additionally, the test expects the command `['fish', '--version']` to be executed instead of `['fish', '-c', 'echo $FISH_VERSION']`, leading to another assertion failure.

### Fix Strategy
To fix the bug, we need to update the command used to retrieve the Fish shell version to extract just the version number from the output. We also need to correct the expected command in the test to match the actual command being executed.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(' ')[2].replace(',', '')  # Extract version number
    return u'Fish Shell {}'.format(version)
``` 

After making this change, the function should correctly extract and return the Fish shell version number without any extra text. This will ensure that the test passes as expected.