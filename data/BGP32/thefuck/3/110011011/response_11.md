### Identified Bug:
The bug lies in the `info` function of the `Fish` class in the `fish.py` file. The function tries to extract the version of the Fish shell by running the command `fish -c 'echo $FISH_VERSION'` and then decoding the output from the process. However, the function is not correctly handling the output of the command, leading to an incorrect version string being returned.

### Error Cause:
The error occurs because the `Popen` mock object's `stdout.read()` method is returning a `MagicMock` object instead of the actual output of the command. This `MagicMock` object is causing the version variable to be set to `'fish, version 3.5.9'` instead of just `'3.5.9'`. As a result, the assertion in the test fails because the expected output is `'Fish Shell 3.5.9'` while the function is returning `'Fish Shell fish, version 3.5.9'`.

### Fix Strategy:
To fix the bug, we need to modify the `info` function to correctly extract the version string by parsing the output of the command. We can split the output based on the delimiter `,` and then extract the version part. This will ensure that only the version number is returned and not any additional text.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version_output = proc.stdout.read().decode('utf-8').strip()
        
        version = version_output.split(',')[1].strip().split()[1]
        
        return u'Fish Shell {}'.format(version)
```

By splitting the `version_output` based on `,`, we can extract the version number correctly. This corrected version of the `info` function should now return the expected output `'Fish Shell 3.5.9'`.