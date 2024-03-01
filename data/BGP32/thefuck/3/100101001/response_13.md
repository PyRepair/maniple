The issue in the buggy function lies in the command used to retrieve the version of the Fish shell. The command is 'echo $FISH_VERSION', but in the test case, it expects the version to be retrieved using 'fish --version'.

To fix the bug, we need to update the command in the Popen call to 'fish --version'.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return 'Fish Shell {}'.format(version)
```

With this fix, the function will now correctly retrieve the version of the Fish shell using 'fish --version' command as expected by the test case.