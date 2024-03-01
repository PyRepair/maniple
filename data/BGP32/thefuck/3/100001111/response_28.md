## Bug Explanation
The bug in the `info` function arises from incorrectly parsing the version information returned by executing the command `echo $FISH_VERSION`. The current implementation includes the string `'fish, version'` in the version output, which is not expected. This leads to incorrect version information being included in the final output, causing issues when the plugin interacts with Oh-My-Fish.

## Bug Fix Strategy
To fix this bug, we need to adjust the parsing of the version information to only extract the version number from the output of the `echo $FISH_VERSION` command. By removing the unwanted text and retaining only the version number, we can ensure that the output matches the expected format.

## Corrected Version of the Function
Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().replace('fish, version ', '')
    return u'Fish Shell {}'.format(version)
```

This corrected version addresses the parsing issue by removing the unnecessary text from the version output, ensuring that only the version number is included in the final output. This fix aligns with the expected output values and resolves the reported issue with the plugin interacting with Oh-My-Fish.