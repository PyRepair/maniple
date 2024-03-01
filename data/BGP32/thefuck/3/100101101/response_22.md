## Bug Explanation
The bug in the `info` function stems from the fact that the command used to retrieve the Fish shell version is incorrect. The command should be `fish --version` instead of `fish -c 'echo $FISH_VERSION'`. This discrepancy leads to a mismatch between the expected version format and the actual version extracted from the command output.

## Fix Strategy
To fix the bug, we need to update the command in the `Popen` call to `['fish', '--version']` so that it correctly returns the Fish shell version in the expected format.

## Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1].replace(',', '')
    return u'Fish Shell {}'.format(version)
```