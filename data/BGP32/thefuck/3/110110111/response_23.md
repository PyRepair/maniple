Based on the information provided, we can see that the bug lies in the `Fish.info` function. The function is trying to extract the version of Fish shell using the command `fish -c 'echo $FISH_VERSION'`, but in the failing test, the expected output does not match the actual output.

The buggy function is not capturing the correct output from the process and is including additional text which causes the assertion to fail.

To fix this bug, we need to correct the command used to get the Fish shell version and ensure that only the version number is extracted from the output.

Here is the corrected version of the `Fish.info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will properly extract the version number from the command output, and the failing test will pass successfully. This fix addresses the issue reported on GitHub related to the recursive loop triggered by using the command in the `Fish.info` function.