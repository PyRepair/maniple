Based on the provided information, the bug in the `info` function is due to the usage of the incorrect command in the `Popen` call. The command `['fish', '-c', 'echo $FISH_VERSION']` should be replaced with `['fish', '--version']` to correctly retrieve the version of the Fish Shell.

Additionally, the way the output of the `Popen` call is being read and decoded should be reviewed to ensure it accurately captures the version information.

Here's the corrected code for the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return 'Fish Shell {}'.format(version)
```

With this fix, the `Popen` call now uses the correct command to retrieve the version of the Fish Shell, and the output is read and decoded properly. This updated function should resolve the bug and provide the expected output for the test case.