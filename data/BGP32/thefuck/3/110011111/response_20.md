## Bug Explanation

The buggy function `info()` in the `Fish` class is trying to retrieve the Fish shell version by executing the command `echo $FISH_VERSION`. However, the output is not being processed correctly, leading to an assertion error in the test case due to the unexpected format of the version string.

The error message states that the actual output is `'Fish Shell fish, version 3.5.9'` while the expected output is `'Fish Shell 3.5.9'`. This discrepancy is due to not properly extracting only the version number from the command output.

## Bug Fix Strategy

To fix the bug, it is necessary to extract only the version number from the output of the command `echo $FISH_VERSION`. This can be achieved by parsing the string to isolate the version number and then formatting it correctly in the return statement.

## Corrected Version

Here is the corrected version of the `info()` function in the `Fish` class:

```python
class Fish(Generic):

    def info(self):
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        
        # Extract the version number from the output
        version_parts = version.split(', version ')
        if len(version_parts) > 1:
            version = version_parts[1]
            
        return u'Fish Shell {}'.format(version)
```

This corrected version first splits the version string based on `', version '`, and if the split results in two parts, it considers the second part as the actual version number. This ensures that only the version number is included in the final output, resolving the discrepancy observed in the failing test.