### Identified Bug:
The bug in the `info` function stems from how the version of Fish shell is extracted from the stdout of the process. The current implementation expects the output to be just the version number, but it actually includes extra text "fish, version".

### Cause of the Bug:
1. The subprocess Popen is initiated to run the command `fish -c 'echo $FISH_VERSION'`.
2. The output of this command includes extra text "fish, version" before the version number.
3. The function then tries to extract and format just the version number, leading to the mismatch between the expected and actual output.

### Fix Strategy:
To fix the bug, we need to modify the way we extract the version number from the stdout. We should split the output by `,` and then extract the version from the resulting list.

### Corrected Version:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    # Split the output by comma and get the second part containing the version
    parts = output.split(',')
    version = parts[1].strip() if len(parts) > 1 else ''  # Check if version is present
    return u'Fish Shell {}'.format(version)
```

This corrected version handles the scenario where the output contains extra text before the version number. It splits the output by comma and extracts the version number from the resulting parts.