### Bug Fix Strategy:
The issue is arising because the `info` function in the `fish.py` file is returning the version string with extra characters like "fish, version" included. To fix this issue, we need to modify the line where we are extracting the version information so that only the version number is returned without any extra characters.

### Correction:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]  # Extract just the version number
    return u'Fish Shell {}'.format(version)
```

By splitting the version string and extracting the last part, we ensure that we only return the version number itself, removing any extra characters. This correction should resolve the failing test case and align with the expected output values.