## Identify the Bug
The bug in the `info` function lies in the command used to fetch the Fish Shell version. The current command `echo $FISH_VERSION` returns additional text along with the version number which is causing the comparison to fail in the test.

## Cause of the Bug
- In the failing test, the expected version number is `'3.5.9'`, but the actual version extracted from the `echo $FISH_VERSION` command includes extra text, resulting in the assertion failure.
- The test command `['fish', '--version']` does not match the actual command `['fish', '-c', 'echo $FISH_VERSION']` used in the `info` function.

## Fix Strategy
1. Modify the command `['fish', '-c', 'echo $FISH_VERSION']` to output only the version number without any additional text.
2. Update the test to match the correct version number extraction from the modified command.

## Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    # extract only the version number
    version = version.replace('fish, version ', '')
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will extract only the version number without extra text, matching the expected version. Additionally, adjust the test to validate the corrected version extraction.