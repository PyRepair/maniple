## Identification:
1. The bug occurs in the `info` function of the `Fish` class within the `fish.py` file.
2. The bug is causing the assertion error in the test where the expected version `'3.5.9'` is being compared with the version number retrieved from the shell output `'fish, version 3.5.9'`.
3. The expected output should be `'Fish Shell 3.5.9'`, but due to the issue in the function, it is not formatted correctly.

## Bug Cause:
The bug is caused by the incorrect formatting of the version number extracted from the shell output. The function `info` is not correctly parsing and reformatting the version number before appending it to the shell name.

## Strategy for Fixing the Bug:
To fix the bug, we need to modify the function to correctly format and extract only the version number from the shell output before constructing the final string with the shell name.

## The Corrected Version of the Function:
```python
# The corrected version of the buggy function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        # Extract just the version number from the output
        version = version.split(',')[1].strip()
        return u'Fish Shell {}'.format(version)
```

By modifying the function to extract only the version number and ensuring it is correctly formatted, the bug causing the assertion error should be resolved.