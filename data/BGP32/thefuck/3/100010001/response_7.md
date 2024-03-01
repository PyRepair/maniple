### Analysis:
- The error message indicates that the `info` function is returning an unexpected value. The actual value obtained from the subprocess is "fish, version 3.5.9" instead of just "3.5.9".
- The discrepancy between the expected output and the obtained output suggests that the version information retrieved from the subprocess contains extra text (including "Fish Shell").
- The function is supposed to extract the version number from the string "fish, version 3.5.9" and format it as "Fish Shell 3.5.9".

### Bug Fix Strategy:
- The bug in the function lies in the way it is extracting the version number from the output of the subprocess.
- To fix this bug, we need to modify the section of code that reads the output of the subprocess to correctly extract only the version number.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()  # Read the output of the process
    # Extract version number only
    version_start = version.find('version ') + len('version ')
    version = version[version_start:]
    return u'Fish Shell {}'.format(version)
```

### Explanation:
- In the corrected version of the function, the extracted version string obtained from the subprocess output is processed to remove the extra text ("Fish Shell" and comma).
- By finding the index of "version " in the string and extracting the text after it, we ensure that only the version number is included in the formatted output.
- This modification ensures that the final output of the `info` function correctly represents the version number without any extra unnecessary text.