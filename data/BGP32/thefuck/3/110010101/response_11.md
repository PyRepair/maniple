### Analysis
1. The buggy function `info` in the `Fish` class is trying to extract the version of the Fish shell by running a command `fish -c 'echo $FISH_VERSION'` using the `Popen` function.
2. The error occurs due to the incorrect parsing of the output from the `Popen` process. The expected version is `'3.5.9'`, but the extracted version includes extra text `'fish, version'`.
3. The root cause of the bug is the incorrect parsing of the output in the following line:
    ```python
    version = proc.stdout.read().decode('utf-8').strip()
    ```
    The output of the command includes additional text `'fish, version'`, which is not removed correctly.
4. To fix the bug, we need to modify the parsing logic to extract only the version number without any additional text.
   
### Bug Fix
```python
# The corrected version of the info function in the Fish class
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

The fix involves splitting the extracted output by `,` and selecting the second part (index 1) to get only the version number without any additional text. This modification ensures that the function returns the correct version value.