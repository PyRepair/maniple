### Explanation:
The bug in the function is caused by the incorrect formatting of the version string extracted from the command output. The function is currently returning a string that includes the original prefix "fish, version" along with the version number. The expected output is just the version number without any prefix.

### Strategy for fixing the bug:
To fix the bug, we need to modify the extraction of the version number from the command output so that it only includes the version number itself without any additional text.

### Corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', ')[-1]  # Extract only the version number
    return u'Fish Shell {}'.format(version)
``` 

By splitting the output string by ', ' and selecting the last element, we ensure that only the version number is returned without any extra prefixes. This corrected version should now pass the failing test case.