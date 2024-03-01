The issue in the provided code is that the command used to get the version of Fish shell is incorrect, causing the version to be returned as "fish, version 3.5.9" instead of just "3.5.9". This leads to the failing test since the expected output is "Fish Shell 3.5.9", but the actual output contains unnecessary text.

To fix this bug, we need to update the command used to fetch the Fish shell version. Here's the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(' ')[2] # Extracting only the version number
    return f'Fish Shell {version}'
```

By modifying the command to `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`, we ensure that the correct version string is extracted. Additionally, splitting the version string by space and extracting the version number only also helps in obtaining the desired output format.

This corrected version should now pass the failing test case provided.