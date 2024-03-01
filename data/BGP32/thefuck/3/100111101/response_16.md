The bug in the provided function `info` is that it is trying to extract the version information by executing the command `'echo $FISH_VERSION'`, but in the failing test, the version output is `'fish, version 3.5.9\n'`. The function then tries to format this as `'Fish Shell {}'` which causes the assertion error.

To fix this bug, we need to update the command being executed to extract just the version number from the output of `'fish --version'`.

The corrected version of the function is as follows:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.readline().decode('utf-8')
    version = output.split(',')[1].strip().split()[1]
    return 'Fish Shell {}'.format(version)
```

By modifying the command to `'fish --version'`, we can extract the version information from the expected output `'fish, version 3.5.9\n'`. The corrected function will pass the failing test and provide the expected output 'Fish Shell 3.5.9'.