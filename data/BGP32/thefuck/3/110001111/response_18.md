Based on the runtime and expected values provided, the bug in the `info` function of the `Fish` class is that it incorrectly formats the version string retrieved from the shell command. The provided input value for `version` includes the additional text "fish, version" along with the actual version number. The expected output value does not have this additional text and only includes the version number.

To fix this bug, we need to modify the way the version string is processed from the output of the shell command and extract only the version number without any additional text.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    split_version = version.split(", version")
    if len(split_version) > 1:
        version = split_version[1].strip()
    return f'Fish Shell {version}'
```

By splitting the `version` string based on ", version", we can extract only the actual version number without any additional text. This corrected version should now return the expected output without the extra text, resolving the bug.