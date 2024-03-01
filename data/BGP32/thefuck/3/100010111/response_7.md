Based on the provided information, it seems that the bug in the `info` function of the `Fish` class is related to the incorrect handling of the output from the `Popen` process. The function is supposed to extract the Fish Shell version from the output, but it includes additional text "fish, version" which causes the assertion error.

The cause of the bug is that the function is not correctly parsing the output of the `Popen` process to extract only the version number. It is returning the entire output including the text "fish, version".

To fix this bug, we need to modify the function to extract only the version number from the output by splitting the string based on a delimiter (`,` in this case) and then stripping any whitespace characters.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split(',')[1].strip()
    return f'Fish Shell {version}'
```

This corrected version reads the output from the `Popen` process, splits it by `,` to extract the version part (index 1), removes any leading/trailing whitespace, and returns the correct version number.

By updating the function in this way, it should now pass the failing test and return the expected output "Fish Shell 3.5.9" as required.