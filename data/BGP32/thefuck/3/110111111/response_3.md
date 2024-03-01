To fix the bug in the `info` function for the Fish shell, we need to adjust the command being run to extract the version information correctly. Currently, the command `echo $FISH_VERSION` is used, which results in the unwanted string "fish, version" being included in the output. 

We can modify the command to directly get the version using `fish --version`. 

Here is the corrected version of the `info` function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.split()[-1])  # extract only the version number
```

This version of the function should correctly extract the version number and return it without the unwanted additional text. It will address the failing test case and satisfy the expected input/output values.