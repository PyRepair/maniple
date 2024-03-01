### Analysis:
1. The buggy function `info` in the `Fish` class of the `fish.py` file is attempting to get the version of Fish shell using a subprocess call to retrieve the `FISH_VERSION`. However, the current implementation is not correctly parsing and formatting the output.
2. The error message indicates a failing test where the expected output is `'Fish Shell 3.5.9'` but the actual output is `'Fish Shell fish, version 3.5.9'`.
3. The bug is caused due to incorrect parsing of the command output in the `info` function, where the output is not properly stripped and formatted.
4. To fix the bug, we need to correctly parse the output of the command `echo $FISH_VERSION` to extract only the version number without any additional text like `'fish, version'`.

### Fix Strategy:
1. Modify the code to correctly parse the output of the `echo $FISH_VERSION` command to extract only the version number.
2. Update the formatting of the version number in the return statement to match the expected output format `'Fish Shell <version>'`.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', version ')[-1]
        return 'Fish Shell {}'.format(version)
``` 

By parsing the output of the command to extract only the version number, the corrected version should now properly format and return `'Fish Shell <version>'`, passing the failing test and resolving the GitHub issue.