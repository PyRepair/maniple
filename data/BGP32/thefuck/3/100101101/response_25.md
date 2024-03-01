The bug in the provided function lies in the command used to retrieve the Fish shell version. The command being executed is `'echo $FISH_VERSION'`, which does not provide the version string in the expected format. 

To fix this bug, the command should be changed to `'fish --version'` to correctly retrieve the version information of the Fish shell.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return 'Fish Shell {}'.format(version)
```

With this correction, the function will now correctly extract the version information by executing `'fish --version'` and parsing the output to obtain the version number.

This corrected version should pass the failing test case provided.