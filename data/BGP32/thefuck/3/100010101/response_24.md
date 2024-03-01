### Bug Analysis
The bug in the provided function lies in the way the `version` is being extracted from the output of the `Popen` object. The function is currently trying to extract the version by simply reading the stdout of the `Popen` object, but it's not handling the output format correctly. The error message shows that the version retrieved is `'fish, version 3.5.9'` instead of just `'3.5.9'`, which causes the assertion to fail.

### Bug Fix Strategy
To fix this bug, we need to modify the way the version is extracted from the output. Since the output contains additional text like `'fish, version'`, we need to split the output and extract only the version number.

### Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().strip().decode('utf-8')
    version = output.split(', version ')[-1]
    return u'Fish Shell {}'.format(version)
```

By using `output.split(', version ')[-1]`, we split the output by `', version '` and take the last element which should be the version number. This corrected version should now correctly extract and return just the version number.