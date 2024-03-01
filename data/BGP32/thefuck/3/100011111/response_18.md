### Bug Fix Strategy:
- The issue seems to be with the way the version is being extracted from the output of the Popen command.
- The current implementation is adding "Fish Shell" before the extracted version, leading to the incorrect comparison in the test.
- To fix the bug, we need to modify the extraction of the version from the Popen output to only include the version number without any additional text.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.replace('fish, version ', '')  # Extracting only the version number
    return u'Fish Shell {}'.format(version)
``` 

This corrected version extracts only the version number from the output and then formats it along with "Fish Shell" to match the expected output in the test.