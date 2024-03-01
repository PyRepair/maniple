## Analysis
1. The buggy function `info` in the `Fish` class is supposed to return the name and version of the current shell, which should be fetched by running a command to retrieve the version. 
2. The `info` function makes a subprocess call to retrieve the version of Fish shell by running the command `fish -c 'echo $FISH_VERSION'`.
3. The failing test is checking if the returned version matches the expected version ('Fish Shell 3.5.9'). The error message shows that the actual output contains additional characters ("fish, version") which is not expected.
4. The bug is in how the version output is retrieved from the subprocess call.
   
## Bug Explanation
When the subprocess call is made to get the Fish shell version, the returned output includes additional text "fish, version". This leads to the actual output not matching the expected output in the test, causing the assertion error.

## Fix Strategy
To fix the bug, we need to modify the subprocess call to only retrieve the version number without including any additional text. This can be achieved by modifying the command passed to Popen to request `fish --version` instead of `echo $FISH_VERSION`.

## Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version_output = proc.stdout.read().decode('utf-8').strip()
        version = version_output.replace('fish, version ', '')  # Extract version number from the output
        return u'Fish Shell {}'.format(version)
```

With this corrected version, the `info` function should now properly fetch the Fish shell version from the subprocess call, allowing the `test_info` test function to pass successfully.