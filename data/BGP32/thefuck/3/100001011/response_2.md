### Error Location:
The error in the `info` function lies in reading the output of the process (`proc.stdout.read().decode('utf-8').strip()`). This can cause the function to hang in certain scenarios, such as when using the `thefuck -v` command with Oh-My-Fish plugin.

### Bug Cause:
The bug is causing the function to hang due to reading the process output without handling the potential for the process to hang or be blocked.

### Strategy for Fixing the Bug:
To fix the bug, the function should wait for the process to complete before reading its output to prevent the hanging issue.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    proc.wait()  # Wait for the process to complete
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By adding `proc.wait()` after starting the process, the function ensures that the process completes before trying to read its output. This fix prevents the function from hanging when executing commands like `thefuck -v` with the Oh-My-Fish plugin.