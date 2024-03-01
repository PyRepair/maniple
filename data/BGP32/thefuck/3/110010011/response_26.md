### Analysis:
- The `info` method in the `Fish` class is attempting to retrieve the version of the Fish shell using a subprocess call, but the command used to extract the version seems to be incorrect.
- The error message indicates that the version retrieved includes extra information (e.g., 'fish, version'), which causes the assertion to fail.
- The GitHub issue mentions that the `info` method is causing a recursive loop issue when Oh-My-Fish plugin uses `thefuck -v`.

### Potential Error Locations:
- The command `echo $FISH_VERSION` being used to get the version of Fish shell.
- The way the version information is being extracted and formatted in the `info` method.

### Bug Cause:
- The `echo $FISH_VERSION` command is returning not just the version number but also additional text like 'fish, version'. This extra text is causing the mismatch in the expected result.
- As a result, when the version is formatted with 'Fish Shell' prefix in the return statement, it is not matching the expected result.

### Strategy for Fixing the Bug:
- Change the command used to retrieve the version of the Fish shell to only return the version number without any additional text.
- Update the extraction and formatting logic in the `info` method to handle the version information correctly.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        # Extracting version number from format 'fish, version 3.5.9'
        version_number = version.split()[-1]
        return u'Fish Shell {}'.format(version_number)
```

### Explanation of Changes:
- Updated the command to retrieve the version using `echo $version` to only get the version number.
- Extracted only the version number from the output and used it in the return statement with 'Fish Shell' prefix.
- By extracting the version number correctly, the method now returns the expected result of 'Fish Shell 3.5.9'.

### By making these changes, the bug in the `info` method should be fixed and the corrected version should pass the failing test, resolving the issue reported on GitHub.