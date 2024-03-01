The issue with the current `info` function in the `fish.py` file is that it reads the output from the `Popen` process using `proc.stdout.read()`, which can lead to a deadlock if the process doesn't close properly. This deadlock can cause the function to hang, which is the reported problem in the GitHub issue.

To fix this issue, we can modify the function to wait for the process to finish before reading its output. Here's the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    stdout, _ = proc.communicate()
    version = stdout.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By using `proc.communicate()` instead of `proc.stdout.read()`, we ensure that the function waits for the process to complete before reading its output. This change should prevent the function from hanging and resolve the reported issue.

The corrected function should now correctly handle the process communication and return the expected shell name and version without causing any deadlock.