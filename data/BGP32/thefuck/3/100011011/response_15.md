### Analysis:
1. The `info` function is trying to get the version of Fish shell by executing `fish -c 'echo $FISH_VERSION'` command.
2. The function is reading the output using `proc.stdout.read()` which is causing an issue with decoding the output.
3. The error message shows that the actual output contains the version along with additional text, causing the assertion to fail.
4. To fix the bug, we need to modify the way we extract the version to only get the version number.

### Bug Fix:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output, _ = proc.communicate()
    version = output.decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
``` 

By using `proc.communicate()` to get the output and then extracting the version number only, we ensure that unnecessary text does not interfere with the version comparison.