The cause of the bug in the provided code is that the command used to fetch the Fish shell version is incorrect. The command 'echo $FISH_VERSION' should be changed to 'fish --version' to properly get the version of the Fish shell.

To fix this bug, update the command in the Popen call to fetch the Fish shell version correctly. Then, extract and format the version from the output accordingly.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split()[2] if version else ''
    return u'Fish Shell {}'.format(version)
```

This fixed version will correctly retrieve the version of the Fish shell and format it as expected. It should now pass the failing test provided above.