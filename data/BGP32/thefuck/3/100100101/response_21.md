The bug in the `info` function is due to incorrect command arguments passed to `Popen` and an incorrect decoding method for the result. The command used to fetch the version should be `fish --version` instead of `echo $FISH_VERSION`. Additionally, the decoding method `proc.stdout.read().decode('utf-8')` should be replaced with `proc.stdout.readline().decode('utf-8')` to correctly read and decode the output.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.readline().decode('utf-8').strip().split(',')[-1].strip()
    return u'Fish Shell {}'.format(version)
```

By making the changes mentioned above, the function should now correctly fetch the Fish shell version and decode it to return the expected output.

This corrected version should pass the failing test case with the expected input/output values.