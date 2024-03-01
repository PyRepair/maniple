## Analysis
1. The `info()` function in the `fish.py` file is attempting to retrieve the version of the Fish shell but is using the incorrect command (`echo $FISH_VERSION` instead of `fish --version`).
2. The failing test expects the output of `shell.info()` to be `'Fish Shell 3.5.9'`, but due to the incorrect command, the actual output is `'Fish Shell fish, version 3.5.9'`.
3. The assertion error is occurring because the expected and actual output strings do not match.
4. To fix the bug, we need to correct the command used to retrieve the Fish shell version in the `info()` function.

## Bug Fix Strategy
1. Update the command executed by `Popen` to `['fish', '--version']` to retrieve the correct version information.
2. Parse the output of the command to extract the version number.
3. Update the function to return the correct formatted string `'Fish Shell <version>'`.

## Corrected Version of the Function
```python
# The relative path of the corrected file: thefuck/shells/fish.py

def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version_full = proc.stdout.read().decode('utf-8').strip()
    version = version_full.split(' ')[2]
    return u'Fish Shell {}'.format(version)
```

With this correction, the `info()` function should now correctly retrieve the Fish shell version and format it as `'Fish Shell <version>'`, passing the failing test case.