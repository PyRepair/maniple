## Explanation of the bug
The bug in the `info` function of the `Fish` class is caused by incorrectly extracting the version number from the output of the `fish -c 'echo $FISH_VERSION'` command. The current implementation includes the literal `fish, version` in the version string, which is not the expected output format.

Additionally, the issue on GitHub suggests that this incorrect version output is causing a recursive loop when used with the Oh-My-Fish plugin, leading to unexpected behavior and potentially hanging the shell initialization process.

## Bug Fix Strategy
1. Modify the code to correctly extract only the version number from the output of the `fish -c 'echo $FISH_VERSION'` command.
2. Update the return statement to include only the version number without any additional text.
3. Ensure that the function returns the correct version format expected by the callers.

## Corrected Version of the Function
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(", ")[1]  # Extract only the version number
        return version  # Return only the version number
```

With the corrected version above, the function now correctly extracts only the version number from the output of the `fish -c 'echo $FISH_VERSION'` command and returns it without any extra text. This fix should resolve the issue reported on GitHub and prevent the recursive loop when used with the Oh-My-Fish plugin.