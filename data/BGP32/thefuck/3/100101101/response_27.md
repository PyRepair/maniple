## Bug Explanation
The bug in the `info` function arises from the fact that the command used to retrieve the Fish shell version is incorrect. The command `echo $FISH_VERSION` is being used, but the correct command should be `fish --version`. This causes the `version` variable to contain the entire output string including "fish, version" which leads to a mismatch in the expected output.

## Fixing the Bug
To fix this bug, we need to update the command used to retrieve the Fish shell version to `fish --version` instead of `echo $FISH_VERSION`. This will ensure that only the version number is captured in the `version` variable.

## The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
``` 

By making this correction, the `info` function should now return the correct version number without any extraneous information, passing the failing test.