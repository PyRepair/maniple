## Analysis:
1. The `info` function in the `Fish` class is supposed to return the version of the Fish shell by executing a command using `Popen`.
2. The expected output is `'Fish Shell x.x.x'` where `x.x.x` represents the version number.
3. The failing test expects the version number to be extracted from the output `b'fish, version 3.5.9\n'` and formatted accordingly.
4. The bug seems to be related to the command used to retrieve the Fish shell version.

## Bug:
The bug is caused by the incorrect command used to retrieve the Fish shell version. The command `echo $FISH_VERSION` should be replaced with `fish --version` in order to correctly get the version information.

## Fix:
Replace the command used in the `Popen` call with `['fish', '--version']`.

## Corrected Version:
```python
# The corrected version of the info function

def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```