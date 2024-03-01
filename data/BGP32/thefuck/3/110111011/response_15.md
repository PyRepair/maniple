### Explanation:
The current implementation of the `info` function in the `Fish` class of `shells/fish.py` is not correctly retrieving the Fish shell version. The issue lies in the command used to get the Fish version, which should be `'fish', '--version'` instead of `'fish', '-c', 'echo $FISH_VERSION'`. This mismatch causes the function to return unexpected version output leading to test failures.

### Strategy for Fixing the Bug:
1. Update the command used to fetch the Fish version by replacing `['fish', '-c', 'echo $FISH_VERSION']` with `['fish', '--version']`.
2. Modify the `info` function to correctly parse and format the fetched version.
3. Ensure the test case `test_info` in `test_fish.py` reflects the updated functionality by verifying the parsed version against the expected output.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version_parts = version.split(', version ')
        if len(version_parts) > 1:
            version_number = version_parts[1]
            return f'Fish Shell {version_number}'
        return 'Fish Shell Unknown Version'
```

With this corrected implementation, the `info` function retrieves the Fish shell version correctly and formats it as expected. It should now pass the failing test case.