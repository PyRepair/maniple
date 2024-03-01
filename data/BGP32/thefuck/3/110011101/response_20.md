The bug in the provided function arises due to the incorrect extraction of the version information from the output of the `fish -c 'echo $FISH_VERSION'` command. The function currently retrieves the entire output, including the unnecessary text "fish, version" before the version number.

To fix the bug, we need to extract only the version number from the output and return it in the correct format.

Here is the corrected version of the function:

```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The corrected class containing the fixed function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version_info = proc.stdout.read().decode('utf-8').strip()  # read the output
        version_number = version_info.split(',')[1].strip()  # extract the version number
        return f'Fish Shell {version_number}'
```

With this correction, the function will correctly extract only the version number from the command output and return it in the format `'Fish Shell {version_number}'`. This should now pass the failing test and provide the expected output 'Fish Shell 3.5.9'.