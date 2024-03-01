### Explanation of the bug
The bug in the provided function arises due to the incorrect handling of the subprocess `Popen` object. The function correctly creates a subprocess to retrieve the version of the Fish shell, but it fails to properly read the output from the subprocess and decode it before returning the shell's version.

### Strategy for fixing the bug
To fix the bug, we need to ensure that the subprocess output is read and decoded correctly before returning the shell's version. This involves modifying how the function interacts with the `Popen` object and its output.

### Corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_bytes = proc.stdout.read()
    proc.stdout.close()
    version = version_bytes.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

In the corrected version:
1. We read the output of the subprocess `Popen` and store it in `version_bytes`.
2. We then close the `stdout` pipe to release any resources associated with it.
3. Finally, we decode the `version_bytes` to a UTF-8 string and strip any extra whitespace before returning the formatted shell version.