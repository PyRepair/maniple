The bug in the `info` function is caused by the way it retrieves the Fish shell version and constructs the return string. The issue arises from the fact that the version includes additional information such as "fish, version" along with the actual version number, which leads to incorrect output.

To fix the bug, we should modify the function to extract only the version number from the output of the command 'echo $FISH_VERSION'. We can achieve this by splitting the output based on whitespace and taking the last element, assuming that the version number is the last part of the string.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

This updated version should now correctly extract and display only the Fish shell version number without any additional text. It aligns with the expected output values mentioned in the test cases.