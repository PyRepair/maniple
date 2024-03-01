### Explanation:
The bug in the `info` function lies in the command used to extract the Fish shell version. The command should be `'fish', '--version'` instead of `'fish', '-c', 'echo $FISH_VERSION'`. This is evident from the failing test, which asserts the expected output format of the version string.

### Strategy for fixing the bug:
1. Modify the command sent to Popen to fetch the Fish shell version by using `['fish', '--version']`.
2. Update the parsing logic to extract the version number properly by removing any unnecessary text.

### Corrected version of the `info` function:
```python
# The corrected version of the buggy function in the thefuck/shells/fish.py file

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version_info = proc.stdout.read().decode('utf-8').strip()
        version = version_info.split(' ')[-1]
        return f'Fish Shell {version}'
``` 

By making these changes, the function will correctly retrieve the Fish shell version and return it in the expected format, thus passing the failing test.