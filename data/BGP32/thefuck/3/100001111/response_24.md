The bug in the provided function lies in how the version of the Fish shell is extracted using the 'echo $FISH_VERSION' command. The extracted version includes additional information, such as 'fish, version', which should be stripped to only include the version number.

The strategy for fixing this bug involves modifying the extraction of the version to only capture the version number without any additional text.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(", ")[1]
    return u'Fish Shell {}'.format(version)
```

This corrected version modifies the extraction of the version by splitting the retrieved string using ', ' and selecting the second part, which represents only the version number. This ensures that the output matches the expected value without any additional text.