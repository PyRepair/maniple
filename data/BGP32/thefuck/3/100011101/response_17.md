## Bug Explanation
The bug in the `info` function is caused by not correctly parsing the version information obtained from the command `echo $FISH_VERSION`. The current implementation is not handling the output string properly, which results in including unwanted text in the version number.

The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output contains extra text like `'fish, version'` before the version number.

## Bug Fix Strategy
To fix the bug, we need to extract only the version number from the output obtained from the command `echo $FISH_VERSION`. We can achieve this by splitting the output string and getting only the part that represents the version number.

## The corrected function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split(',')[1].strip().split()[1]
    return u'Fish Shell {}'.format(version)
```

By splitting the version output string on `','` and extracting the second element, we can then split the resulting string based on whitespace and retrieve the actual version number. This corrected version of the function should now correctly extract the version number and return `'Fish Shell 3.5.9'`.