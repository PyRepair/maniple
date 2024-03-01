The bug in the provided function occurs because the `Popen` object's `stdout` attribute is not being accessed correctly to retrieve the output of the command. Instead of using `proc.stdout.read().decode('utf-8').strip()`, we should use `communicate()` method to get the output from the process. 

Here's a corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    stdout, _ = proc.communicate()
    version = stdout.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

This corrected version properly retrieves the output of the command using `communicate()` method, decodes it to a string, and then formats it with the version string.