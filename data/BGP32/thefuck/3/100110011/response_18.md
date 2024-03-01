### Analysis:
1. The `info` function in the `fish.py` file is attempting to get the version of Fish shell by running the command `fish -c 'echo $FISH_VERSION'`. However, in the failing test, the expected version string is different from the actual output.
2. The failing test is mocking the output of the command `fish --version` to be `b'fish, version 3.5.9\n`, but the `info` function is trying to read the version with a different command.
3. The error message shows that the assertion fails because the expected output contains the version number only, without any additional "fish, version" text.
4. To fix the bug, we need to make sure that the `info` function reads the correct output from the mocked command.

### Fix Strategy:
Modify the `info` function in the `fish.py` file to run `fish --version` command instead of `fish -c 'echo $FISH_VERSION'` to retrieve the correct version format that matches the expected output in the failing test.

### Corrected Version:
```python
# The corrected version of the function in the file: thefuck/shells/fish.py

def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will extract only the version number from the output of `fish --version` command. This should align with the expected version format in the failing test, thereby fixing the bug reported in the GitHub issue.