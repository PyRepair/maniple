The bug in the provided function `info` is due to the incorrect extraction of the Fish shell version. The function is trying to extract the version directly from the output of the command `'echo $FISH_VERSION'`, which includes additional information like 'Fish Shell'. This causes an issue when the version is being compared in a test scenario, as the expected version does not match the actual version extracted.

To fix this bug, we need to modify the extraction process to only retrieve the version number without any additional text.

Here is the corrected version of the function `info`:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version_parts = version.split(' ')  # Split the version string by space
    return f'Fish Shell {version_parts[-1]}'  # Return only the version number
```

By splitting the version string by space and returning only the last part (which should be the version number), we ensure that the extracted version matches the expected version correctly. This fix aligns with the details provided in the GitHub issue regarding the incorrect extraction of the Fish shell version causing a recursive loop.