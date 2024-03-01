## Analysis:
1. The `info` function is attempting to extract the version of Fish shell by running the command `echo $FISH_VERSION` using the subprocess `Popen`.
2. The failing test sets up a mock for `Popen` to return `b'fish, version 3.5.9\n'`, but the `info` function reads this input using `proc.stdout.read()` and expects only the version number.
3. The bug occurs because the `info` function is not correctly parsing the output to extract just the version number, resulting in a mismatch with the expected output in the test.
4. To resolve this bug, we need to modify the `info` function to extract only the version number from the command output.

## Bug Fix:
```python
# Fix the buggy function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

In the fixed version, the command to retrieve the version has been changed from `'echo $FISH_VERSION'` to `'fish --version'` to obtain the complete version string. Then, the version number is extracted by splitting on the comma and retrieving the version part only.

This fix will make the `info` function correctly parse the version number from the shell command output, allowing it to pass the failing test.