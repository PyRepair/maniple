## Bug Explanation
The bug in the provided `info` function is due to the fact that the version string extracted from the output of the `fish -c 'echo $FISH_VERSION'` command contains additional text ("fish, version") that is not expected in the final output. This extra text is causing the assertion error in the failing test.

## Fix Strategy
To fix the bug, we need to modify the way we extract the version information from the output of the `fish -c 'echo $FISH_VERSION'` command. We need to parse the output string to extract only the version number without the unnecessary text.

## The corrected version of the function

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(", version ")[1]  # Extract only the version number
    return u'Fish Shell {}'.format(version)
```

With this modification, the `info` function should now correctly extract the version number from the output and return it as 'Fish Shell 3.5.9', passing the failing test.