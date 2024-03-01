### Fixing the Bug
- The bug in the `info` function is due to the incorrect command used to get the Fish shell version. The correct command should be `echo $FISH_VERSION`, not `--version`.
- Additionally, the version string extracted from the output includes both "fish" and "version". We need to extract only the version number from this string.
- To fix the bug, we need to change the command used with Popen to get the Fish shell version and modify the version extraction logic.

### Corrected Version
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):
    
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version_output = proc.stdout.read().decode('utf-8').strip()
        # Extract only the version number from the output
        version = version_output.split()[-1]
        return f'Fish Shell {version}'
```

After correcting the `info` function with the changes mentioned above, the function should now correctly extract the version number from the Fish shell output and return the expected result.

This corrected version should pass the failing test provided.