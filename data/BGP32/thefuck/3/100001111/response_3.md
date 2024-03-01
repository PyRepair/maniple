The bug in the `info` function is caused by the incorrect output parsing when trying to get the version of the Fish shell. According to the runtime values and types, the `version` variable includes unnecessary information like the text "fish, version" that needs to be removed to match the expected output.

To fix this bug, we should modify the parsing logic to extract only the version number from the output. Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.replace('fish, version ', '')  # Remove unnecessary text
    return u'Fish Shell {}'.format(version)
```

This corrected version properly extracts and formats the version number from the output of the `fish -c 'echo $FISH_VERSION'` command. It will provide the expected output and address the issue reported on GitHub related to the recursive loop triggered by the incorrect version extraction.