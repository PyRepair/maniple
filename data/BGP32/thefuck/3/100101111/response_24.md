The bug in the `info` function arises from reading the output of the `fish -c 'echo $FISH_VERSION'` command using `proc.stdout.read().decode('utf-8').strip()`. The expected output is `'fish, version 3.5.9\n'`, but the function is trying to extract only the version number without parsing the full output correctly.

The strategy to fix this bug is to correctly parse the version number from the output of the `fish -c 'echo $FISH_VERSION'` command. This can be achieved by splitting the output based on the comma and space characters to isolate the version number.

Here is the corrected version of the `info` function that will pass the failing test:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(', version ')[1].strip().replace('\n', '')
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will correctly extract the version number from the output and return `'Fish Shell 3.5.9'` as expected. This fix addresses the parsing issue and ensures the function behaves as intended.