The bug in the `info` method of the Fish shell is causing a recursive loop when the plugin is used, leading to unexpected behavior and hanging. The problem is likely in the command that retrieves the version of the Fish shell using Popen. The expected output is 'Fish Shell 3.5.9' but the actual output is 'Fish Shell fish, version 3.5.9' due to an incorrect command used to retrieve the version.

To fix the bug:
1. Modify the Popen command to use the correct command to retrieve the Fish shell version.
2. Ensure that the command returns the expected output format 'Fish Shell x.x.x'.

Here's the corrected code for the `info` method:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-v'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(' ')[2]  # Extract the version number
    return u'Fish Shell {}'.format(version)
```

This correction uses the `fish -v` command to retrieve the version of the Fish shell and extracts the version number from the output before returning a string in the expected format 'Fish Shell x.x.x'. This fix should resolve the issue reported in the GitHub repository.