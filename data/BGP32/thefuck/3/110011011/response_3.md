### Analysis:
1. The `info` function in the `Fish` class is meant to return the name and version of the current shell by running a subprocess command.
2. The error message shows that the expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`.
3. The test fails because the returned version includes unnecessary text from the subprocess output.
4. We need to modify the function to extract only the version number from the subprocess output without additional text.

### Bug Cause:
The bug is caused by directly using the output of the subprocess without filtering out unwanted text. The version extracted includes extra text leading to the assertion failure in the test case.

### Fix Strategy:
1. Modify the function to extract only the version number from the output of the subprocess command.
2. Filter out any unwanted text and return only the version number.
3. Ensure that the returned string matches the expected format.

### Corrected Version:
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(", ")[1]
        return u'Fish Shell {}'.format(version)
```

This corrected version includes splitting the output of the version command to extract only the version number. It filters out the unnecessary text, ensuring that the function returns the expected format.