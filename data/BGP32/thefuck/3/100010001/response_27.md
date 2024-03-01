## Analysis
The error message indicates that the `info()` function is returning the shell name and version in an unexpected format. The expected version string is `'Fish Shell 3.5.9'`, but the actual version string being returned is `'Fish Shell fish, version 3.5.9'`. This suggests that the `u'Fish Shell {}'.format(version)` statement in the `info()` function is not formatting the version correctly.

## Error Location
The issue lies in how the output of the `Popen` command is being read and processed in the `info()` function. It seems like the `echo $FISH_VERSION` command is outputting additional text along with the version number, which is causing the version string to be formatted incorrectly.

## Cause of the Bug
The `echo $FISH_VERSION` command is returning the version number along with the shell name and additional text. This extra text is not being removed before formatting the version string, leading to the unexpected output.

## Fixing the Bug
To fix the bug, we need to update the `info()` function to properly extract and format the version number from the output of the `Popen` command.

## Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(", version ")[1]  # Extract only the version number
    return 'Fish Shell {}'.format(version)
```

By splitting the output string based on `", version "`, we can extract only the version number part and use it to format the correct version string. This corrected version of the `info()` function should now pass the failing test.