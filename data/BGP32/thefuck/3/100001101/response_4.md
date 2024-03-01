The bug in the provided function lies in the way the version string is extracted from the output of the `fish -c 'echo $FISH_VERSION'` command. The current implementation of the function is not correctly parsing the version string leading to an incorrect output.

To fix the bug, we need to parse the output of the command properly to extract only the version number and return it. Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    if 'fish, version' in output:
        version = output.split('fish, version ')[1]
        return f'Fish Shell {version}'
    else:
        return 'Fish Shell (unknown version)'
```

With this corrected version, the function will properly extract the version number from the command output and return it along with the shell name. This should satisfy the expected input/output values for the given cases.