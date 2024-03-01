To fix the bug in the `info` function in `fish.py` of `thefuck`, we need to address the following issues:

1. The command used to retrieve the Fish shell version is incorrect. It should be `'fish', '--version'` instead of `'fish', '-c', 'echo $FISH_VERSION'`.
2. The extraction logic for the version from the command output is incorrect.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]  # Extracting version correctly
    return u'Fish Shell {}'.format(version)
```

By making these changes, the function will correctly retrieve the version of the Fish shell and format it appropriately. This corrected version should now pass the failing test case and satisfy the expected input/output values.