The bug in the `info` function of the `Fish` class in `fish.py` is with the command used to obtain the version of Fish shell. The issue arises from using `'echo $FISH_VERSION'` in the Popen call instead of `'fish --version'`. This causes the version output to include unnecessary text ('fish, version') which leads to the failing test.

To fix this bug, the Popen call should be updated to use `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(", version ")[1]
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will properly extract the version from the output and return 'Fish Shell 3.5.9' as expected in the failing test. This fix will also address the GitHub issue related to the recursive loop triggered by incorrect version extraction.