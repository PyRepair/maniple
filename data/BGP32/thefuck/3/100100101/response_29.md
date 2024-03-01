The bug in the `info` function lies in the command used to get the Fish shell version. The command should be `'fish --version'` instead of `'echo $FISH_VERSION'`. This change will ensure that the correct version string is extracted from the command output.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By modifying the command to `'fish --version'`, the function will fetch the correct version string from the command output and return the expected result 'Fish Shell 3.5.9'.

After making this correction, the failing test case should pass successfully without any assertion errors.