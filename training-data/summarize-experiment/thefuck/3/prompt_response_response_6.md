Based on the test case provided and the error message, it seems that the bug is related to the incorrect extraction of the version number from the output of the 'fish --version' command. The error message indicates that the expected version is 'Fish Shell 3.5.9' but the actual output is 'Fish Shell fish, version 3.5.9'.

The cause of this bug is that the 'fish --version' output is not being parsed correctly in the `info` function.

To fix this bug, we can modify the `info` function to properly parse the version number from the output of the 'fish --version' command.

Here's the revised version of the fixed function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(' ')[2]  # Extracting the version number from the output
    return f'Fish Shell {version}'
```

This revised function uses the `--version` option instead of `-c` to run the 'fish' command and properly extracts the version number from the output using the `split` method. This should resolve the bug and provide the expected output.