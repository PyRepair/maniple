### Analysis
1. The error message shows that the `info` function is returning the version of Fish shell in a format that includes the word "fish" before the version number. This is causing the assertion error.
2. The function uses `echo $FISH_VERSION` command to retrieve the Fish shell version, but the output includes the word "fish, version" before the actual version number.
3. The expected output is a string in the format 'Fish Shell x.x.x', where 'x.x.x' represents the version number.
4. To fix the bug, we need to modify the `info` function to extract only the version number from the output.

### Bug Fix Strategy
1. Update the `info` function to strip the unwanted text and keep only the version number extracted from the process output.
2. Modify the returned string to include the correct format 'Fish Shell x.x.x'.

### The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(' ')[-1]
    return u'Fish Shell {}'.format(version)
```