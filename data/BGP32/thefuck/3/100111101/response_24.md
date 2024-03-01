### Analysis:
1. The `info` function is designed to retrieve the version of the Fish shell using the `FISH_VERSION` environment variable.
2. The failing test expects the version to be returned in the format `'Fish Shell x.x.x'`.
3. The failing test indicates that the actual output includes extra text `"fish, version"` before the version number.
4. The cause of the bug is due to the incorrect parsing of the output from the command `echo $FISH_VERSION`.
5. To fix the bug, we need to extract only the version number from the output.

### Updated Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].strip().split(' ')[1]
    return f'Fish Shell {version}'
```

With this update, we split the output on commas, take the second part, split on spaces, and take the second part again to extract just the version number without the extra text. This change should make the function return the version in the expected format.