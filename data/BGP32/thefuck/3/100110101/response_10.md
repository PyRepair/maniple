The bug in the provided function `info` lies in the command used to retrieve the Fish Shell version. The command `echo $FISH_VERSION` does not provide the correct version string, which leads to an incorrect output in the function. 

To fix this bug, we need to change the command to `fish --version` as expected in the failing test. This command will output the correct version string, which can then be parsed and used in the function to return the correct shell name and version.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will now retrieve the correct Fish Shell version and return the expected output.