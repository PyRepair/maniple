## Analysis:
The main issue with the buggy function `info` is that it is trying to fetch the fish version using `echo $FISH_VERSION` command instead of `fish --version`. This mismatch leads to incorrect version extraction and hence the failing test case.

## Bug Cause:
1. The function `info` is using incorrect command to fetch the version of the Fish shell (`echo $FISH_VERSION` instead of `fish --version`).
2. Due to the wrong command, the extracted version is not correct ('fish, version 3.5.9' instead of '3.5.9').
3. The mismatch in versions causes the failing test since the result is not as expected.

## Fix Strategy:
- Modify the command in the `info` function to use `fish --version` instead of `echo $FISH_VERSION` to fetch the correct shell version.

## Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(",")[1].strip())
```

By making the above correction, the function should now properly fetch the Fish shell version and pass the failing test case.