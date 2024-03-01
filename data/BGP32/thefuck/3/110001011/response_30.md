### Identified Bug:
The bug in the `info` function of the `Fish` class is caused by reading the output of the `Popen` process incorrectly. This leads to the function not returning the correct version of the Fish shell and causing issues with the Oh-My-Fish plugin.

### Bug Cause:
The bug is caused by using the `proc.stdout.read()` method directly to get the output of the process, which can sometimes result in incomplete or incorrect output being read. This can lead to the incorrect version being returned or the function hanging in certain cases.

### Fix Strategy:
To fix this bug, it is advisable to use the `communicate()` method on the `Popen` process to properly capture the output. This method ensures that the process is fully completed and all output is captured correctly, preventing any potential issues with incomplete reads.

### Corrected Version:
Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    stdout, _ = proc.communicate()
    version = stdout.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By using `proc.communicate()` to capture the output of the process, we ensure that the function retrieves the correct version of the Fish shell without any potential issues. This correction should resolve the problem reported in the GitHub issue related to the Oh-My-Fish plugin.