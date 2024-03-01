### Analysis
1. **Buggy Function**: The `info` function in the `Fish` class is supposed to return the name and version of the current shell `Fish`. It runs a subprocess to fetch the version information and then formats it as a string with the shell name.
   
2. **Failing Test**: The failing test is checking if the function correctly retrieves the version information and formats it as expected.

3. **Error Message**: The error message shows that the actual output of the function includes extra text "fish, version" which shouldn't be there. This indicates that the function is not correctly extracting and parsing the version number.
   
4. **Expected Input/Output**:
   - When the subprocess runs, it should return the version number only.
   - The `info` function should format the version number as `'Fish Shell x.x.x'`.

### Bug Cause
The bug is caused by the incorrect extraction of the version number from the output of the subprocess. The function is not handling the version string correctly, resulting in unexpected additional text in the final formatted output.

### Strategy for Fixing the Bug
1. Modify the function to correctly extract only the version number from the output of the subprocess.
2. Update the formatting of the extracted version number in the return statement to match the expected output.

### Corrected Version
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        
        # Extract just the version number
        version = output.split(' ')[-1] if 'version' in output else 'Not Found'
        
        return u'Fish Shell {}'.format(version)
```

Fixing the bug involves correctly parsing the output of the subprocess to extract only the version number and formatting it in the desired way. Now, the corrected version of the function should pass the failing test and return the expected output.