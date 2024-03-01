The bug in the `info` function comes from the incorrect command used to retrieve the Fish shell version. The command being run in the `Popen` call is using `echo $FISH_VERSION`, which is not the correct way to fetch the Fish version.

To fix this bug:
1. Modify the command in the `Popen` call to use `fish --version` instead of `echo $FISH_VERSION` to get the correct version of the Fish shell.
2. Update the decoding logic to handle the version output correctly.

Here is the corrected version of the `info` function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.replace('fish, version ', '').replace('\n', '')
    return f'Fish Shell {version}'
```

With this correction, the `info` function should now correctly retrieve the Fish shell version using `fish --version` and pass the failing test provided.