## Analysis
The buggy function `info(self)` in the `Fish` class is supposed to retrieve the version of the Fish shell by running a command and then formatting the output to return the version number appended with "Fish Shell". 

1. The function uses `Popen` to run the command `fish -c 'echo $FISH_VERSION'` to get the version of Fish shell.
2. It then reads the output from the command, decodes it and trims the whitespace.
3. Lastly, it formats the version number with "Fish Shell" and returns it.

The failing test asserts that the output of `shell.info()` should be `'Fish Shell 3.5.9'`. However, the test fails with an AssertionError because the function output includes extra text `fish, version` which is not expected.

## Bug
The bug here is in the way the version number is extracted from the output. The function is currently extracting the whole output and trimming it, instead of just extracting the version number.

## Fix
To fix the bug, the function needs to extract only the version number from the output, which can be achieved by splitting the output and then selecting the relevant part.

## The corrected version of the function:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version_output = proc.stdout.read().decode('utf-8').strip()
        version = version_output.split(', version ')[-1].strip()
        return u'Fish Shell {}'.format(version)
``` 

This corrected version will properly extract and return the version number of the Fish shell.