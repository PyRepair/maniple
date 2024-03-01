## Analyzation
1. The buggy function `info` in the `Fish` class is attempting to retrieve the version of the Fish shell using a subprocess. The issue arises because it is trying to extract the version string from the output, which includes unnecessary information.
2. The issue affects the proper functioning of the shell information retrieval in the `Fish` class for the `thefuck` project, causing a recursive loop when triggered by certain plugins.
3. The bug occurs due to the incorrect extraction of the version string in the subprocess output and the nature of the output itself.
4. To fix the bug, we should modify the command passed to the subprocess so that it only outputs the version number itself without any additional information.

## Bug Fix
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)  # Modify the command to extract version directly
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]  # Extract just the version number
        return u'Fish Shell {}'.format(version)
```

By modifying the command in the subprocess to use `--version` option, we can directly extract the version number without any unnecessary information. Then, we extract just the version number part to return the correct shell version information.

This fix should address the bug reported in the GitHub issue and provide the expected output without causing any recursive loops.