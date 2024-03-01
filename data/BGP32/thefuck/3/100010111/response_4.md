### 3. Explanation of the bug

The bug in the `info` function of the `Fish` class in `shells/fish.py` is caused by the way the version output is being read and formatted. The error message shows that the expected version is `3.5.9`, but the actual output includes unwanted additional information like `fish, version`. This discrepancy is due to the incorrect handling of the output from the `fish -c 'echo $FISH_VERSION'` command. 

The current code reads the entire output of the subprocess and then strips it. However, since the output contains more than just the version number, the formatting is incorrect.

### 4. Strategy for fixing the bug

To fix this bug, we need to modify how we capture and format the version information from the subprocess output. One approach is to parse the output to extract just the version number before formatting it into the desired string.

### 5. Corrected version of the function

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    
    # Extract the version number from the output
    version = version.split(',')[1].strip()

    return u'Fish Shell {}'.format(version)
```

In this corrected version, we first capture the output from the subprocess, then split the string using the comma `,`. This allows us to extract the version number part (after the comma) and strip any extra spaces. Finally, we format the extracted version number into the desired output string and return it. This approach ensures that only the version number is used for formatting in the return statement.