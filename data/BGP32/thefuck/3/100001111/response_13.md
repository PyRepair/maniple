The bug in the provided function is that it reads the output from the `Popen` process without waiting for the process to finish. This can lead to unexpected behavior, such as incomplete or incorrect output being read. Additionally, the function is not properly stripping the version number from the output.

To fix this bug, we need to wait for the `Popen` process to finish before reading the output. We also need to properly extract and format the version number from the output.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    proc.wait()  # Wait for the process to finish
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(', version ')[1]  # Extract the version number
    return u'Fish Shell {}'.format(version)
```

This corrected version ensures that the process is finished before reading the output. It also properly extracts and formats the version number from the output. This should fix the issue reported on GitHub related to the recursive loop triggered by the `thefuck -v` command in the Fish Shell.