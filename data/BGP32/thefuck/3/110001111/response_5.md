### Analysis
1. **Relationship:** The `info` function is part of the `Fish` class in the `fish.py` file under the `shells` directory in `thefuck` project.
   
2. **Runtime I/O:** The function uses `Popen` to run a command in the Fish shell and retrieve the version. However, the decoding of the output and the formatting of the return string seem to be causing issues.

3. **Expected I/O:** The function is expected to correctly extract the version number from the output of the command and return it formatted as `'Fish Shell version_number'`.

4. **GitHub Issue:** The function is causing a recursive loop when the `thefuck -v` command is used, likely due to incorrect handling of the command output.

### Bug Location
The bug likely originates from the decoding and parsing of the output from the `Popen` command. The current implementation does not handle the output correctly.

### Bug Cause
The buggy function is not decoding the output of the `Popen` command properly, leading to the version including unwanted extra text. This incorrect version format causes issues when trying to use it in the context specified by the GitHub issue.

### Strategy for Fixing the Bug
1. Modify the decoding process to extract only the version number without any extra text.
2. Update the formatting of the return string to adhere to the expected format.

### Corrected Version
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
        return u'Fish Shell {}'.format(version)
```

This corrected version properly extracts just the version number from the output of the `Popen` command and formats it as `'Fish Shell version_number'`. This should resolve the issue noted in the GitHub bug report.