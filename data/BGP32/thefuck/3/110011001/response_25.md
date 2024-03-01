### Identified Bug

The bug in the `info` function of the `Fish` class is caused by the fact that the output of the `Popen` subprocess is not being properly decoded and stripped before formatting it into the final return value. This results in the unwanted prefix `'fish, version '` remaining in the `version` variable.

### Fix Strategy

To fix this bug, we need to properly decode the output of the `Popen` subprocess and remove the prefix before formatting it into the final return value.

### Corrected Version

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().replace('fish, version ', '')
        return f'Fish Shell {version}'
```