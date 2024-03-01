### Analysis:
1. The buggy function `info` in the `Fish` class from the `thefuck.shells.fish` module is attempting to get the version of the Fish shell by executing a command in a subprocess.
2. The error message indicates that the output of the command is not being processed correctly, leading to a version string that includes unnecessary text.
3. The error message shows that the output of the `echo $FISH_VERSION` command includes extra text like "fish, version" which is not required.
4. To fix the bug, we need to modify the way the output is read and processed from the subprocess.
5. We need to strip the unnecessary text and only extract the version number.

### Bug Fix Strategy:
1. Modify the Python code that reads the output from the subprocess to extract only the version number part.
2. Ensure that the extracted version number is used in the correct format to generate the output string.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()  # Read the output and strip any extra characters
        version_components = version.split()  # Split the output to extract version number
        if len(version_components) >= 2:
            version = version_components[1]  # Get the version number
        return u'Fish Shell {}'.format(version)
```

This corrected version reads the output from the subprocess, removes any extra characters, extracts the version number, and uses it to generate the correct output string. This version should now pass the failing test and resolve the issue reported on GitHub.