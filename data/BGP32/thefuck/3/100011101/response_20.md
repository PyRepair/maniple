### Analysis
The buggy function `info` is currently returning the entire output of the `fish -c 'echo $FISH_VERSION'` command, including the text "fish, version". This causes the assertion error in the test since the expected output does not include this text.

The `version` variable is being extracted incorrectly from the output of the command. It should only contain the version number, without the extra text.

### Solution
To fix the bug, we need to extract only the version number from the command output and return it as the shell's version.

### The corrected version of the function

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(", version ")[-1]
    return u'Fish Shell {}'.format(version)
```

The corrected version of the `info` function will now properly extract the version number without the additional text and return it as expected. This version should pass the failing test.