### Analysis
The issue in the `info` function lies in how it reads the output from the `Popen` process. The `proc.stdout.read()` method is being called before the process has completed, resulting in an empty output. This causes the `version` variable to be an empty string.

### Bug Explanation
The `Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)` command starts a process to execute `echo $FISH_VERSION` in the Fish shell. However, calling `proc.stdout.read()` immediately after starting the process does not wait for the process to complete, leading to an empty output and an incorrect version value.

### Bug Fix
To fix this bug, we need to wait for the process to complete before reading its output. This can be achieved by using the `communicate()` method on the process object, which waits for the process to complete and then returns a tuple of stdout and stderr streams. We can then extract the stdout stream and decode it to get the version value.

### Corrected Version

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    stdout, _ = proc.communicate()
    version = stdout.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```