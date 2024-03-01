### Analysis:
1. The buggy function `info` in the `Fish` class of the `fish.py` file is trying to get the version of the Fish shell by running the command `echo $FISH_VERSION` using the Popen module.
2. The error message indicates that the expected output from the `shell.info()` call is `'Fish Shell 3.5.9'`, but the actual output contains additional characters `'fish, version 3.5.9'`.
3. The cause of the bug is the incorrect handling of the shell output. The function is returning the entire line of the command output instead of extracting and formatting just the version number.
4. To fix the bug, we need to parse the version number from the output of the command and format it correctly as `'Fish Shell 3.5.9'`.

### Bug Fix:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        # Read the output of the command
        output = proc.stdout.read().decode('utf-8').strip()
        
        # Extract the version number using split
        version = output.split(',')[1].strip()

        return 'Fish Shell {}'.format(version)
```

### Explanation:
1. The fixed function reads the output from the `Popen` process and strips any whitespace.
2. Then, it extracts the version number by splitting the string at the comma and taking the second part (version number).
3. Finally, it formats and returns the `Fish Shell` string with the extracted version number.
4. This fix ensures that only the version number is extracted and formatted correctly before returning. The corrected function should now pass the failing test.