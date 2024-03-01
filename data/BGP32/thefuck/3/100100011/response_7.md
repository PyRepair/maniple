## Analysis:
- The `info` function in the `fish.py` file is intended to return the name and version of the Fish shell by executing a command.
- The function is currently trying to read the output from the process created by `Popen` without waiting for the process to finish, which can lead to incorrect or incomplete output.
- The failing test is setting the expected output of the `Popen` call to `['fish', '--version']`, but the actual command being executed is `['fish', '-c', 'echo $FISH_VERSION']`.

## Bug Cause:
- The bug is caused by incorrect command execution in the `info` function and not correctly handling the process output.

## Fix Strategy:
1. Update the command being executed by `Popen` to `['fish', '--version']`.
2. Ensure that the process output is properly read and decoded before returning the version.

## Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    stdout, _ = proc.communicate()
    version = stdout.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

With this corrected version, the command to get the Fish Shell version is `['fish', '--version']` and the process output is correctly handled before returning the version. This should resolve the issue and the failing test.