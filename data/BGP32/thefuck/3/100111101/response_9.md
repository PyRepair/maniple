The bug in the `info` function is caused by trying to extract the version number from the output incorrectly. The expected version is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`.

To fix this bug, we need to modify how we extract the version number from the output of the `fish -c 'echo $FISH_VERSION'` command. We should extract just the version number part and not include any extra information.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[-1]  # Extract only the version number
    return u'Fish Shell {}'.format(version)
```

By splitting the extracted version on `', version '` and taking the last part, we get just the version number itself.

This fix should make the failing test pass as the correct version number will now be extracted from the output.