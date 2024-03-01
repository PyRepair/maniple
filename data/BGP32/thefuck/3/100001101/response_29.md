## Analysis
The buggy function is trying to retrieve the version of the Fish shell by executing a command and reading the output. However, it seems that the version string retrieved includes extra information that needs to be stripped to match the expected value. The function is returning the version with extra text, causing the test to fail.

## Bug Cause
The bug is caused by not properly formatting the version string extracted from the output of the executed command. The expected version is `'3.5.9'`, but the actual version retrieved includes extra text like `'fish, version 3.5.9'`.

## Strategy for Fixing the Bug
To fix the bug, we need to modify the way we extract the version from the output of the command. Instead of returning the entire string, we should extract only the version number itself.

## The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(", ")[1]
    return u'Fish Shell {}'.format(version)
```

By splitting the version string based on `", "` and selecting the second part, which contains only the version number, we can ensure that the function returns the expected value.