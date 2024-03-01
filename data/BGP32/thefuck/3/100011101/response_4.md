### Analysis
- The buggy function is using `Popen` to run a command in the Fish shell to get the version, but the returned version includes unnecessary text.
- The `assert` statement is failing because the expected output is `'Fish Shell 3.5.9'` but the actual output includes additional text.
- The `strip()` method is missing in the current implementation, which causes the extra text to be included in the version string.
- The `version` variable is not correctly extracted from the output of the command.

### Fix
- Add the `strip()` method to the `version` variable to remove any leading or trailing whitespaces.
- Extract only the version number from the output string using appropriate methods.

### The corrected version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(', version ')[1]  # Extracting only the version number
    return u'Fish Shell {}'.format(version)
```