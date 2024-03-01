Based on the provided buggy function and failing test, it appears that the issue lies in how the version of the Fish shell is retrieved and formatted in the `info` function. The test expects the version number to be extracted after the keyword "version" and formatted as 'Fish Shell x.x.x', but the current implementation does not account for this.

To fix the bug, we need to update the way the version is extracted from the output of the subprocess call. We should modify the command used to get the Fish shell version and then extract the relevant information.

Here is the corrected version of the `info` function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```

Explanation of the changes:
1. Changed the command to `['fish', '--version']` to ensure we get the correct version information.
2. Extracted the version number using `output.split(', version ')[1]` after splitting the output at ', version '.

This corrected function should now pass the failing test by extracting the version number correctly and formatting it as 'Fish Shell x.x.x'.