## Explanation

The bug in the `info` function of the `Fish` class is caused by the fact that the command used to get the version of the Fish shell is incorrect. The command `echo $FISH_VERSION` does not return the version in the expected format (`3.5.9`). This results in the incorrect comparison when testing the output in the test function.

Additionally, the expected value of the version in the test function is `3.5.9` without the preceding `fish, version` text, which further highlights the discrepancy between the actual output and the expected output.

## Fix Strategy

To fix this bug, we need to update the command used to extract the version of the Fish shell. Instead of using `echo $FISH_VERSION`, we can simply use `fish --version` which directly provides the version information without additional text. This modification will ensure that the version extracted matches the expected format.

## The corrected version of the function

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(", version ")[1])
```

By updating the command to `fish --version`, we can accurately extract the version information and format it correctly to match the expected output in the test function. This correction should resolve the failing test case and align the function with the expected behavior.