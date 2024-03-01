### Analysis:
The issue in the provided function arises from the handling of the `Popen` object and its `stdout`.

1. The `Popen` object `proc` is created with the command `['fish', '-c', 'echo $FISH_VERSION']`, which should fetch the Fish Shell version. However, the read operation on `proc.stdout` is not managed correctly, leading to potential issues in retrieving the version information.

2. The usage of `decode('utf-8')` on `proc.stdout.read()` to convert the byte output to a string may cause encoding-related problems if not handled properly.

### Bug Cause:
The primary cause of the bug is improper handling of the `Popen` object's output stream (`stdout`) when trying to read the Fish Shell version.

### Fix Strategy:
1. Ensure that the output from the `Popen` object is read properly to avoid potential blocking issues.
2. Handle the decoding of the byte output from `stdout` appropriately to prevent encoding-related errors.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_bytes = proc.stdout.read()
    version = version_bytes.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

In the corrected version, we first read the output bytes from `proc.stdout` and then decode them to a string using `utf-8` encoding. The `strip()` method is used to remove any leading/trailing whitespaces before returning the Fish Shell version information.