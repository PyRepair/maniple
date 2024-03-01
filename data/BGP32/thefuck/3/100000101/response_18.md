The bug in the provided function stems from trying to read from `proc.stdout` multiple times without handling the pipeline properly. This can lead to unexpected behavior, such as returning an empty string or None instead of the actual version number.

To fix this bug, we need to communicate with the subprocess by using `communicate()` method after calling `Popen()` and retrieve the output and error streams. This will ensure that the process is properly executed and the output is captured correctly.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    out, _ = proc.communicate()
    version = out.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

This corrected version ensures that the output of the subprocess is properly captured and decoded to obtain the version number of the Fish shell.