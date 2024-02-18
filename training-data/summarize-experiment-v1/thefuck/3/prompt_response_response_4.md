The bug in the function `info` of the `fish.py` file in the `thefuck` repository causes a recursive loop that hangs when the `TheFuck` plugin is used with the Fish shell and the Oh-My-Fish plugin.

To fix this bug, we need to correct the function to retrieve the version of the Fish shell in a way that does not trigger a recursive loop.

Here's the corrected implementation of the `info` function in `fish.py`:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-v'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

With this fix, the `info` function should now correctly retrieve the version of the Fish shell without causing a recursive loop, resolving the issue with the `TheFuck` plugin.

The corrected code addresses the Github issue:

- Title: "thefuck -v hangs Fish Shell initialisation with Oh-My-Fish plugin"
- Detailed Description: "Oh-My-Fish's TheFuck plugin uses thefuck -v to decide when to regenerate functions. That triggers a recursive loop because of shells/fish.py:Fish.info(). Fix is on its way. Reference: oh-my-fish/plugin-thefuck#11"