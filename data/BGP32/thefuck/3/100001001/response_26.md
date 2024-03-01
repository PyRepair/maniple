### Issue:
The bug is likely due to the incorrect handling of the `Popen` process in the `info` function. The function reads the output of the process incorrectly, resulting in an incorrect version value being returned.

### Fix:
To fix the bug, we should properly communicate with the `Popen` process and retrieve the output in a reliable way.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output, _ = proc.communicate()
    version = output.decode('utf-8').strip()
    return 'Fish Shell {}'.format(version)
``` 

With this correction, the `communicate()` method is used to ensure that the entire output of the process is retrieved before decoding it and stripping any unnecessary characters. This approach should provide the correct version value for the Fish shell.