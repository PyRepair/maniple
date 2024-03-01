### Bug Analysis:
1. The `info` function in the `fish.py` file is supposed to return the version of the Fish shell by executing the command `echo $FISH_VERSION`.
2. The test is failing because the expected output is `'Fish Shell 3.5.9'`, but the function is returning `'Fish Shell fish, version 3.5.9'`. The issue lies in the extraction of the version from the command output.
3. The function is reading the output of the subprocess as a string without properly handling the extraction of the version number.
4. To fix the bug, we need to correctly extract and format the version number from the output of the subprocess command.

### Bug Fix:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]  # Extract only the version number
    return u'Fish Shell {}'.format(version)
```

By splitting the output from the subprocess command and extracting the last element (which should be the version number), we can fix the bug that caused the test to fail. This corrected version of the function should now return the expected output `'Fish Shell 3.5.9'` and pass the failing test.