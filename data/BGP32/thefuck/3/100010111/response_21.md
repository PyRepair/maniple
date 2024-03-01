## Analysis
The buggy function `info` is supposed to return the name and version of the current shell, Fish Shell. The function uses a subprocess to run `echo $FISH_VERSION` and extract the version number. However, the bug occurs because the returned value still includes some unnecessary text "fish, version" alongside the version number.

The failing test is expecting the function to return just the version number without any extra text.

## Bug Cause
The bug is caused by the logic in the `info` function which fails to properly extract only the version number from the result of the subprocess call.

## Fix Strategy
To fix the bug, we need to modify the code inside the function to properly extract only the version number. We can do this by splitting the output on the comma and then extracting the second part which should be the version number.

## Corrected Version

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[-1]
    return u'Fish Shell {}'.format(version)
```

After applying the fix, the function should now return only the version number without any additional text, as expected by the failing test case.