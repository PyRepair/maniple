The bug in the provided function is that it is not properly capturing the output of the `fish -c 'echo $FISH_VERSION'` command. The function is attempting to read the output using `proc.stdout.read()`, but this method does not guarantee that all the output will be read at once, leading to potential issues.

To fix this bug, we can use `communicate()` method of the `Popen` object, which will ensure that all the output is read properly.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output, _ = proc.communicate()
    version = output.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

This corrected version uses `communicate()` to read the output of the command properly and then decodes it to get the version information. This should now correctly extract the version of the Fish shell and return it in the expected format.