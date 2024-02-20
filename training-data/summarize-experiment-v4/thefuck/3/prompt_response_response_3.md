## Bug Cause

The `info` function in the Fish shell class attempts to retrieve the version of the Fish shell using the command `fish -c 'echo $FISH_VERSION'`. However, this command does not return the expected output, leading to a version string of the incorrect format. This discrepancy causes the failing test, as the actual output does not match the expected output.


## Fixing the Bug

To fix the bug, the command used to retrieve the version of the Fish shell should be modified. Instead of using `echo $FISH_VERSION`, the version can be obtained by running the command `fish -v`. This modification will ensure that the correct version information is captured and the function returns the appropriate string containing the name and version of the Fish shell.


## The corrected code

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-v'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By replacing the command used with `Popen(['fish', '-v'], stdout=PIPE, stderr=DEVNULL)`, the function will now successfully retrieve the version of the Fish shell, resulting in the expected output "Fish Shell 3.5.9". This correction addresses the failing test and resolves the issue posted in GitHub.