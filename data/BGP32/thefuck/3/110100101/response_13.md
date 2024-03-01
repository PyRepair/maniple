The bug in the `info` function is that the command used to get the version of Fish shell is incorrect. Instead of using `'echo $FISH_VERSION'`, it should be `'fish --version'` to retrieve the version information.

To fix this bug, we need to update the command in the `Popen` call to `'fish --version'`.

Here is the corrected version of the `info` function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
``` 

By updating the command to `'fish --version'`, the function will correctly fetch the Fish shell version information and return it in the expected format. This correction should make the failing test pass.