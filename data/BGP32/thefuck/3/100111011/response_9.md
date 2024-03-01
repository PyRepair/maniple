### Analysis:
1. The buggy function `info()` is intended to return the name and version of the current shell, but it fetches the version by running `fish -c 'echo $FISH_VERSION'` command which returns the version along with some unnecessary text like "fish, version 3.5.9". This causes the assertion error in the failing test.
2. The failing test expects the output to be in the format `'Fish Shell 3.5.9'` without the unnecessary text.
3. The assertion error occurs because the actual output includes the unnecessary text "fish, version" along with the version number while the expected output is just the version number.
4. To fix the bug, we need to modify the way the version is fetched from the shell command output to exclude the unnecessary text.

### Bug Fix Strategy:
Modify the function to extract only the version number from the command output without any additional text.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    
    split_output = version_output.split(', version ')
    if len(split_output) > 1:
        version = split_output[1]
    else:
        version = version_output

    return u'Fish Shell {}'.format(version)
```

Now, the corrected version of the `info()` function will extract just the version number from the command output, removing any unnecessary text. This modification should make the function return the expected output and pass the failing test.