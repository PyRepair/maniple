The bug in the `info` function is due to the incorrect command used to retrieve the Fish Shell version. The command being executed is `'echo $FISH_VERSION'`, but the test is expecting to execute `'fish --version'`. This discrepancy causes the version string to be wrongly formatted in the output.

To fix the bug, we need to update the command used to retrieve the Fish Shell version to `'fish --version'` within the `info` function.

### Corrected Version of the Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```

By making this correction, the `info` function will correctly fetch the Fish Shell version using `'fish --version'` as expected by the test case. This change will address the formatting issue and ensure that the function returns the correct version string.