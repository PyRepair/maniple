## Bug Explanation
The bug in the `info` function is caused by the fact that the command used to retrieve the Fish shell version is incorrect. The function is running `echo $FISH_VERSION` to get the version, but in the failing test, it is expecting the version to be retrieved using `fish --version`. This mismatch in the commands being run is leading to the test failure.

## Fix Strategy
To fix the bug, we need to modify the command being executed by `Popen` to use `fish --version` instead of `echo $FISH_VERSION`.

## The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(',')[1].strip()
    return f'Fish Shell {version}'
``` 

By correcting the function to use `fish --version` command to get the version and then extracting the version from the output correctly, the function should now return the expected result and pass the failing test.