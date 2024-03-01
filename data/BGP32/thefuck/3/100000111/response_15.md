### Analysis:
The buggy function `info` in `fish.py` is attempting to get the version of Fish Shell by executing a command. However, the function is hanging at `proc.stdout.read()` which is causing the recursive loop mentioned in the GitHub issue.

### Error Location:
The issue lies in the way the function is trying to read the output of the subprocess `proc`. The `read()` method is blocking the execution, causing the hang.

### Cause of the bug:
The bug is caused by the blocking behavior of the `read()` method on `proc.stdout`.

### Bug Fix Strategy:
To fix this bug, we need to read the output of the `proc` subprocess in a non-blocking manner to prevent the function from hanging. One way to achieve this is by using `proc.communicate()` method to interact with the subprocess.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    stdout, _ = proc.communicate()
    version = stdout.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
``` 

With this corrected version, the function will read the output of the `fish -c 'echo $FISH_VERSION'` command in a non-blocking manner using `proc.communicate()`, resolving the hang issue mentioned in the GitHub ticket.