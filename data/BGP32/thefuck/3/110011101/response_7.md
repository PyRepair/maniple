### Bug Analysis:
The bug in the `info` function lies in how the version information is extracted from the subprocess output. The current implementation includes the string `'fish, version'` in the version retrieved, leading to a mismatch with the expected output.

### Bug Explanation:
- The `proc` variable represents the subprocess object created using `Popen` to run the command `fish -c 'echo $FISH_VERSION'`.
- The `version` variable is derived from reading the output of the subprocess and decoding it. In the provided runtime values, the `version` variable includes the unwanted string `'fish, version'`.
- This unwanted string in the `version` variable leads to a mismatch when formatting the final output in the return statement.

### Bug Fix Strategy:
To fix the bug, the unwanted string `'fish, version'` needs to be removed from the `version` variable before formatting it in the return statement. This can be achieved by extracting only the version number portion from the output.

### Corrected Version:
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        
        # Extracting only the version number from the output
        version_number = version.split(', version ')[1] if ', version ' in version else version
        
        return u'Fish Shell {}'.format(version_number)
``` 

By extracting and using only the version number (`'3.5.9'`) when formatting the final output, the corrected version of the function will provide the expected output `'Fish Shell 3.5.9'`.