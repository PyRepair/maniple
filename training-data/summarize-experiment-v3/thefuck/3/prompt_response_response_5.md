## Bug's Cause

The bug is caused by using the incorrect command to retrieve the Fish shell version within the `info` function. This results in the returned version being formatted incorrectly and not matching the expected output.

## Fixing the Bug

To fix the bug, the `Popen` command should be modified to use the correct command to retrieve the version of the Fish shell.

## Corrected Code

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'fish --version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By changing the command to `fish --version`, the `info` function will correctly retrieve the version of the Fish shell and return it in the expected format. This change should resolve the issue reported on GitHub and ensure that the test case for the `info` method in the Fish shell passes without any errors.