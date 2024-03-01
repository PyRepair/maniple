### Bug Explanation
The bug in the `info` function is due to the fact that it is trying to read the value of the `FISH_VERSION` environment variable using the command `echo $FISH_VERSION`, but the test is expecting the version to be extracted from the output of `fish --version`.

### Bug Fix Strategy
To fix this bug, we need to modify the command used to extract the version from the output of `fish --version` instead of relying on the `FISH_VERSION` environment variable.

### The Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split()[2]  # Extracting the version from the output
    return u'Fish Shell {}'.format(version)
``` 

With this correction, the `info` function will parse the output of `fish --version` to extract the version number and format it correctly as 'Fish Shell x.x.x'. This modification should ensure that the failing test passes.