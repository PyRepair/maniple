## Analysis:
1. The `info` function is attempting to get the version of the Fish shell by running a command `'fish -c echo $FISH_VERSION'` using the `Popen` function from the subprocess module.
2. The error occurs because the output of the command is not being correctly processed, resulting in an incorrect version string.
3. The error message clearly shows that the expected version string is `'Fish Shell 3.5.9'` but the actual version string obtained is `'Fish Shell fish, version 3.5.9'`.
4. To fix this bug, we need to ensure that the correct parsing of the output is done so that only the version number is extracted.
   
## Bug Fix:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(',')[1].strip().split()[1]  # Extracting the version number
    return u'Fish Shell {}'.format(version)
```

By splitting the output string based on commas and white spaces, we can extract the correct version number from the output. This will ensure that the correct version string is returned by the `info` function.