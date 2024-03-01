The bug in the provided function lies in reading the stdout from the Popen process before it is complete. The read() method is being called on the stdout instance of Popen prematurely, resulting in an incomplete or incorrect output.

To fix this bug, you can use the communicate() method of the Popen object, which waits for the process to finish and returns a tuple containing the stdout and stderr values.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    stdout, _ = proc.communicate()
    version = stdout.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By using `communicate()` instead of directly reading from stdout, the function will now properly wait for the process to finish and retrieve the correct version information before returning it.