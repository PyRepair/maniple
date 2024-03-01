### Analyzing the buggy function and error message:
- The function is trying to retrieve the version of the Fish shell by running a command in the shell and capturing the output.
- The error message indicates that the current implementation is not correctly parsing the version string to just extract the version number.
- The error message specifically shows that the output includes the whole string "fish, version 3.5.9" instead of just the version number "3.5.9".
- This discrepancy causes the assertion error because the expected output is "Fish Shell 3.5.9", while the actual output contains extra text.
- The `decode('utf-8').strip()` part of the code is not correctly removing the unwanted characters.

### Bug Fix Strategy:
- Modify the code to correctly parse and extract only the version number.
- Use a more precise method to extract the version number from the output.

### Corrected Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

By using `split()[-1]`, we ensure that the version number is extracted correctly even if there are extra characters in the output. This modification should resolve the bug and produce the expected output.