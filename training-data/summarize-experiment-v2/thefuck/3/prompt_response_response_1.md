The problem with the current implementation of the `info` function in the `Fish` class is that it is not correctly capturing the version of the Fish Shell. The command used to capture the version is incorrect, resulting in a mismatch between the expected and actual version in the test.

The `info` function is supposed to capture the Fish Shell version using the command `fish --version`, but it is currently using `echo $FISH_VERSION` instead, causing the version to be incorrectly captured.

To fix this bug:
1. Update the command in the `info` function to capture the Fish Shell version correctly using `fish --version`.
2. Ensure that the output of the command is parsed and formatted correctly to match the expected output in the test.

The corrected code for the `info` function in the `Fish` class should look like this:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(' ')[-1])
```

After making this change, the function should capture the Fish Shell version correctly and match the expected value in the test. This fix resolves the issue reported in the GitHub bug by correctly capturing the Fish Shell version and preventing any recursive loops.