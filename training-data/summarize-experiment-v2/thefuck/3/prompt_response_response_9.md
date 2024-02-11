The issue seems to be with the command used to retrieve the version of the Fish shell in the `info` function. The function is currently using `echo $FISH_VERSION` to get the version, but the test is expecting the output of `fish --version`.

The problem originates from the command used to fetch the Fish shell version. The actual input/output variable value and the expected input/output variable value are different. The function uses a different command to fetch the version compared to what the test expects.

To fix the bug, the command to retrieve the version of the Fish shell in the `info` function should be changed to `fish --version`. This will align the function with the expected output in the failing test and resolve the discrepancy.

Here's the corrected code for the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

With this change, the function should pass the failing test as it now aligns with the expected input/output variable information provided. Additionally, it resolves the issue posted in GitHub related to the recursive loop triggered by the previous implementation of the `info` function.

The GitHub issue title for this bug:
```
thefuck -v hangs Fish Shell initialisation with Oh-My-Fish plugin
```

The GitHub issue's detailed description:
```
Oh-My-Fish's TheFuck plugin uses thefuck -v to decide when to regenerate functions. That triggers a recursive loop because of shells/fish.py:Fish.info().

Fix is on its way.

Reference: oh-my-fish/plugin-thefuck#11
```