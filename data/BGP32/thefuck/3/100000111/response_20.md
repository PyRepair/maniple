The bug in the provided function `info` is caused by not closing the pipe opened with Popen after reading the output from the command. This leads to a resource leak and the function might hang in certain scenarios. 

To fix this bug, we should add a `proc.communicate()` call after reading the output to ensure that the pipe is closed properly. This will prevent potential issues related to resource leaks.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    proc.communicate()  # Close the pipe
    return u'Fish Shell {}'.format(version)
```

By adding `proc.communicate()` after reading the output, we ensure that the pipe is closed properly, resolving the resource leak issue mentioned in the GitHub post.