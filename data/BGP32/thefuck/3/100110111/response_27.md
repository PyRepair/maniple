## Identify the bug
The bug in the `info` function of the `fish.py` file is caused by the incorrect command used to retrieve the Fish version. The `Popen` call is using `echo $FISH_VERSION` instead of `fish --version` to get the Fish version.

## Explanation of the bug
- **Buggy Function**: The `info` function is executing the `fish -c 'echo $FISH_VERSION'` command to get the Fish version.
- **Failing Test**: The failing test sets the side effect of `Popen.return_value.stdout.read` to `b'fish, version 3.5.9\n'` and checks if the output of `shell.info()` is `'Fish Shell 3.5.9'`.
- **Error Message**: The assertion fails because the actual output contains the unnecessary text "fish, version" before the version number.
- **Expected Input/Output**: The expected output should be `'Fish Shell 3.5.9'` without any additional text.

## Fix Strategy
To fix the bug, the `Popen` call should be changed to execute `fish --version` to retrieve the Fish version. This will ensure that only the version number is extracted without any additional text.

## The Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[2]
    return u'Fish Shell {}'.format(version)
```

By changing the command to `'fish --version'` and adjusting how the version is extracted from the output, the corrected version of the function should now return the expected output.