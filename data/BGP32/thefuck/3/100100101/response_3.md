The bug in the `info` function lies in the command used to retrieve the version of the Fish shell. The command `'echo $FISH_VERSION'` does not output the shell version in the expected format. It should be changed to `'fish --version'` to correctly obtain the version information.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

With this correction, the function should now properly retrieve the Fish shell version and pass the failing test case provided.