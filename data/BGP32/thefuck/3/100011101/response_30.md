### Explanation:
The bug in the `info` function is caused by the incorrect formatting of the version string obtained from the `fish` command. The version obtained includes additional text "fish, version" which is not needed in the final output. This extra text causes the assertion to fail because the expected output does not contain it.

### Fix strategy:
To fix the bug, we need to modify the code to extract only the version number from the output of the `fish` command.

### The corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(", ")[-1]  # Extracting only the version number
    return u'Fish Shell {}'.format(version)
```

By splitting the version string obtained from the command output and extracting only the version number, we ensure that the output of the `info` function matches the expected output.