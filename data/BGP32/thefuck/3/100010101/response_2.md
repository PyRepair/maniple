### Fixing the Bug

#### Problem:
The bug in the `info` function is caused by the fact that the output from the `Popen` process is `b'fish, version 3.5.9\n'`, including the text `"fish, version"` which is not expected. The function is then trying to format this whole string which results in the unexpected output.

#### Strategy for Fixing:
To fix this bug, we need to properly extract the version number from the output of the `Popen` process. We can do this by splitting the output by space and taking the last element which should be the version number.

#### Corrected Version:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split()[-1]  # Extract version number from the output
    return u'Fish Shell {}'.format(version)
```

With this change, the function will correctly extract the version number and return `'Fish Shell 3.5.9'`, which matches the expected output.