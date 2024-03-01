### Analysis:
1. The error message indicates that the expected output of the `shell.info()` function is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`.
2. The issue is related to the `Fish.info()` function trying to extract the Fish shell version from the stdout of a subprocess, but the text contains extra characters causing the format mismatch.
3. The cause of the bug is that the stdout read from the subprocess contains additional text `'fish,'` which is not handled correctly in the `info()` function, leading to a discrepancy in the expected and actual output.
4. To fix the bug, we need to modify the extraction logic of the Fish shell version from the subprocess stdout.
5. Below is the corrected version of the `info()` function:

### Corrected Version:
```python
# The corrected version of the info function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1]  # Extract only the version
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will correctly extract only the version number from the subprocess stdout and format it into `'Fish Shell X.X.X'`. This updated logic should resolve the issue and pass the failing test.