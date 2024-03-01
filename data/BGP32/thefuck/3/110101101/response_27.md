### Explanation:
The bug in the `info` function arises from the mismatch between the command used to retrieve the version information and the pattern used to extract the version. The command `'echo $FISH_VERSION'` does not provide the version in the desired format for extraction.

### Strategy for fixing the bug:
1. Change the command to `'fish --version'` to get the version information in a consistent format that can be easily extracted.
2. Update the code to parse the version correctly from the output.

### The corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(' ')[2]  # Extract the version from the output
    return u'Fish Shell {}'.format(version)
``` 

By making these changes, the `info` function should be able to properly extract the version information from the output of the `fish --version` command and pass the failing test.