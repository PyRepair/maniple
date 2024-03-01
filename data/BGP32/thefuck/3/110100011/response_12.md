The issue with the `info` function in the `Fish` class is that it is trying to retrieve the version of Fish shell by executing `echo $FISH_VERSION` but the test case is checking for `'fish, version 3.5.9\n'` string. Furthermore, the `Popen.call_args[0][0]` is not matching the actual command `['fish', '--version']`.

To fix the bug, we should update the command to retrieve the Fish shell version to match the expected output in the test case. Also, we need to correct the call_args comparison to match the actual command executed.

Here is the corrected version of the `info` function:

```python
# The corrected version of the function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

With this correction, the `info` function will correctly retrieve the Fish shell version and the test case will pass.