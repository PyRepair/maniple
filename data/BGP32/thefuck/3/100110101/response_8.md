### Explanation:
The bug in the `info` function arises from using the incorrect command to retrieve the Fish shell version. The function is currently using `echo $FISH_VERSION` which does not return the version directly but the string 'fish, version x.x.x'. This causes the test to fail as it expects only the version number to be returned.

### Bug Fix Strategy:
1. Change the command in the `Popen` call to `['fish', '--version']` to properly capture the version information.
2. Modify the decoding and stripping logic to extract only the version number from the output.

### The corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(',')[1].strip().replace('version', '')
    return u'Fish Shell {}'.format(version)
``` 

After making the above correction, the function should now properly extract and return the correct Fish shell version, resolving the failing test case.