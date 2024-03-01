### Potential Error Locations:
1. The command used in Popen might not be correct.
2. The way the version information is being extracted from the stdout might not be accurate.

### Bug Explanation:
The bug occurs because the command used in Popen to get the Fish shell version is incorrect. It is using 'echo $FISH_VERSION' instead of '--version' which leads to incorrect output extraction. The failing test expects to retrieve the version in the format '3.5.9', but the current implementation extracts it as 'fish, version 3.5.9'.

### Bug Fix Strategy:
1. Update the command in Popen to use '--version' to correctly fetch the version information.
2. Adjust the parsing of the stdout to extract the version number '3.5.9' correctly.

### Corrected Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    # Extract the version number correctly
    version = version.split(' ')[2]
    return u'Fish Shell {}'.format(version)
```

By updating the command to fetch the version and adjusting the extraction logic, the corrected function should now pass the failing test and resolve the GitHub issue related to the incorrect version extraction in the Fish shell plugin.