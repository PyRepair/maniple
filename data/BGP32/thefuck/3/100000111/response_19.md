The bug in the provided function `info(self)` arises from the way it reads the output of the subprocess `Popen`. The current implementation is trying to read the output of `Popen` synchronously, which can cause the function to hang in some cases, like the one reported in the GitHub issue.

To fix this bug, we need to modify the function to wait for the subprocess to complete and then retrieve its output. This can be achieved by calling the `communicate()` method on the `proc` object before reading the output.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    proc.communicate()  # Wait for the subprocess to complete
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

This corrected version ensures that the function properly waits for the subprocess to finish before reading its output. This modification should prevent the hanging issue reported in the GitHub bug.