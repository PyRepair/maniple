The bug in the `info` function is caused by the incorrect parsing of the version output from the `fish -c 'echo $FISH_VERSION'` command. The function is returning `'Fish Shell {version}'`, but it should only return the version number without the 'Fish Shell' prefix.

To fix this bug, we need to modify the parsing of the version string from the output of the `Popen` command.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return version
```

By only returning the version string without the 'Fish Shell' prefix, the function now correctly outputs the version number only. This fix will resolve the issue reported in the GitHub thread and satisfy the expected input/output values.