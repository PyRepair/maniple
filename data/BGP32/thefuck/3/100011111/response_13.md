Based on the analysis provided, the issue with the buggy function `info` in `shells/fish.py` is that it is returning the complete output `fish, version 3.5.9` instead of just the version number `3.5.9`. This discrepancy causes the assertion error in the test case due to the mismatch in the expected and actual output. 

To fix this issue, the function needs to extract only the version number from the output of the command `echo $FISH_VERSION`.

Here is a corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(' ')[-1]
    return u'Fish Shell {}'.format(version)
```

This corrected version of the function will extract the version number by splitting the output string on spaces and taking the last element, which is the version number. This change ensures that the function returns only the version number without any additional text.

By implementing this fix, the function should now return the version number '3.5.9' as expected, passing the failing test case and resolving the GitHub issue related to the buggy behavior.