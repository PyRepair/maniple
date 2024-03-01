### Analysis
The current `info` function in the `fish.py` file is attempting to retrieve the version of the Fish shell by executing a subprocess and capturing the output. However, the way it is implemented leads to potential issues such as hanging the shell initialization process, as mentioned in the GitHub issue.

### Identified Issue
The issue arises from reading the stdout of the `Popen` process without waiting for the process to finish. This can cause the function to hang indefinitely, leading to the reported problem.

### Bug Fix Strategy
To fix this issue, we need to ensure that the `Popen` process is properly handled, and we wait for it to finish before reading the output.

### Corrected Function
Here is the corrected version of the `info` function in the `fish.py` file:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version, _ = proc.communicate()
    version = version.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

In this corrected version, `proc.communicate()` is used to wait for the process to finish and capture the output. This ensures that the function does not hang and correctly retrieves the version of the Fish shell.