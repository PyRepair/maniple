The bug in the provided function `info` is that it is expecting the output of the command `fish -c 'echo $FISH_VERSION'` to contain just the version number, while in reality, it includes the text "fish, version" before the version number. This leads to an assertion error in the test function `test_info`.

To fix this bug, we need to modify the way we extract the version number from the command's output so that it only captures the version number itself.

Here is the corrected version of the function `info`:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').split()[2]
    return u'Fish Shell {}'.format(version)
```

In this corrected version:
1. We are changing the command to `fish --version` so that it outputs the version information directly.
2. We split the output based on spaces and extract the version number located at index 2 (assuming the version number is the third element in the output).

With this correction, the function `info` should now correctly extract the version number and pass the failing test.