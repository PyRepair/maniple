## Analysis
The buggy function `info` in the `fish.py` file is trying to extract the version of Fish Shell by running a subprocess and capturing the output. The error message indicates that the extracted version is not correctly formatted. The expected output is `'Fish Shell 3.5.9'`, but the observed output includes the extra text `'fish, version'`.

The cause of the bug seems to be how the version is extracted from the subprocess output using the command `echo $FISH_VERSION`. The command's output is not just the version number but includes additional text.

## Bug Fix Strategy
To fix the bug, we need to modify the command used to extract the Fish Shell version from the subprocess output. We should change the command to output only the version number itself without any additional text.

## Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].strip()  # Extract only the version part
    return u'Fish Shell {}'.format(version)
```

In the corrected version, after extracting the output from the subprocess, we split it by `,` and extract the second part to get only the version number. This modification should ensure that the extracted version is in the correct format.