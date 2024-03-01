### Analysis
- The function is trying to retrieve the version of the Fish shell by executing a command in Fish's command line.
- The expected version is `'3.5.9'`, but the actual version returned includes additional text `'fish, version'`.
- The `info` function is not correctly parsing the version string from the output of the command.

### Bug Cause
- The bug is caused by the incorrect parsing of the version string from the command output.
- the expected version output is `'3.5.9'`, but the full output includes additional text `'fish, version 3.5.9\n'`.

### Fix Strategy
- Modify the parsing logic to extract only the version number from the output string.
- Update the format string to include only the extracted version number.

### The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_full = proc.stdout.read().decode('utf-8').strip()
    version = version_full.split(',')[1].strip()  # Extract version number
    return u'Fish Shell {}'.format(version)
``` 

By splitting the version output using `','` as a delimiter and taking the second part, we can extract the version number `'3.5.9'` correctly.