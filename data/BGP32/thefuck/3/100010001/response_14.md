### Analysis:
- The function `info` is supposed to return the name and version of the current shell, in this case Fish shell.
- In the provided error message, we see that the function is returning the version with an unnecessary extra prefix "fish, version" in the output instead of just the version number.
- The issue likely occurs in how the version information is retrieved and parsed from the standard output of the `Popen` process.

### Bug Cause:
- The bug is due to the incorrect formatting of the output from the `echo $FISH_VERSION` command. The command outputs "fish, version x.x.x" where the unnecessary "fish, version" prefix is considered along with the actual version number.

### Fix Strategy:
- To fix the bug, we need to modify the logic for parsing the version number to exclude the prefix "fish, version". This can be achieved by splitting the output string on the comma and taking the second part as the version number.

### Corrected Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    # Splitting the version string to exclude prefix "fish, version"
    version_number = version.split(', version ')[1]
    return u'Fish Shell {}'.format(version_number)
```

### Test the Fix:
After applying the corrected function, the test case that failed previously should now pass as the superfluous prefix has been removed from the version number output.