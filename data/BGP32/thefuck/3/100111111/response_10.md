## Bug Fix Strategy
1. The current function uses the command `echo $FISH_VERSION` to retrieve the Fish Shell version, however, the test expects the version number to be extracted from the output `fish, version 3.5.9` which contains additional text.
2. To align the function output with the test expectation, we need to modify the function to extract the version number correctly.
3. It is required to update the test input value to reflect the expected output format.

## Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split(",")[1].strip().split(" ")[1]
    return u'Fish Shell {}'.format(version)
```

By modifying the Popen command to use `'--version'` flag and correctly extracting the version number, the corrected function aligns the output with the expected format for the test case.

Now, the corrected function should pass the failing test case.