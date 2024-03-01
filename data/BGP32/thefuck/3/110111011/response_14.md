### Bug Analysis
- **Buggy Function**: The `info()` function in the `Fish` class is supposed to return the version of the Fish shell by running a command using `Popen` but the command used is incorrect.
  
- **Failing Test**: The failing test checks if the version information retrieved by the `info()` function is correctly formatted.

- **Error Message**: The error occurs because the expected output includes unnecessary text ("fish, version") in addition to the version number.

- **Runtime Values**: At the time of return, the `version` variable contains the full output of the command used to retrieve the version which includes additional text. The test expects only the version number.

### Bug Location
The bug lies in the incorrect command `echo $FISH_VERSION` being used to extract the version information from the Fish shell.

### Bug Cause
The `info()` function retrieves the version information of Fish shell using an incorrect command, including unnecessary text in the output which causes the comparison in the failing test to fail due to the unexpected text.

### Bug Fix Strategy
To fix the bug:
1. Update the command executed by `Popen` to fetch only the version number.
2. Strip any unnecessary text from the output to return only the version number.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.replace('fish, version ', '')  # Remove unnecessary text
        return f'Fish Shell {version}'
``` 

By using `['fish', '--version']` as the command for `Popen`, we can directly extract the version without the unnecessary text. Additionally, by removing the extra text using `replace()`, we return only the version number, resolving the failing test.