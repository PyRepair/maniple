### Analysis
- The error message indicates that the `shell.info()` function is returning `'Fish Shell fish, version 3.5.9'` instead of `'Fish Shell 3.5.9'`.
- The `Popen` object is mocked, and the `stdout.read` method is set to return `b'fish, version 3.5.9\n'`, which is causing the unexpected output.
- The buggy function is not correctly handling the output from the `Popen` command and extracting the version number with unnecessary extra text.

### Bug fix strategy
- Modify the code to properly extract only the version number from the output of the `Popen` command.
- Update the return statement to include the extracted version number in the correct format.

### The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(', version ')[1]
    return 'Fish Shell {}'.format(version)
``` 

By splitting the `output` variable using `', version '` as the separator, we can extract the version number and fix the bug.