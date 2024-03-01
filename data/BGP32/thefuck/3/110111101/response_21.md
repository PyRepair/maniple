The bug in the provided function `info` is due to the incorrect command used to fetch the Fish shell version. The command being used is `echo $FISH_VERSION`, which does not return the version information in the expected format.

To fix the bug, the command needs to be changed to `fish --version` to correctly fetch the Fish shell version information.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return f'Fish Shell {version}'
``` 

This corrected version of the function will correctly fetch the Fish shell version using the `fish --version` command and return it in the expected format.