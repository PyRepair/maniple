### Bug Analysis
- The `info` function in the `Fish` class from `fish.py` is expected to return the version of the Fish shell using the `FISH_VERSION` environment variable.
- The bug in the function is caused by the incorrect command used to retrieve the Fish shell version.
- The failing test sets the expected version to `'Fish Shell 3.5.9'`, but the current implementation returns `'Fish Shell fish, version 3.5.9'`.
- The incorrect version string is due to the use of the command `'echo $FISH_VERSION'` to obtain the shell version, which includes extra text.

### Bug Fix Strategy
To fix the bug, we need to update the command executed by Popen to retrieve only the version number without additional text. The correct command to retrieve the Fish shell version is `'fish --version'`, which provides a cleaner version string that can be processed to extract the actual version number.

### Corrected Version of the `info` function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split(',')[1].strip().replace('version ', '')
    return f'Fish Shell {version}'
```

This corrected version of the function will execute the correct command to retrieve the Fish shell version and extract only the version number from the output.