## Identified Bug
The bug in the provided function `info` is that it reads the output of the `Popen` command without closing it, leading to unexpected behavior. This results in the test failing because the actual output includes additional information ("fish, version") compared to the expected output ("3.5.9").

## Bug Fix Strategy
To fix this bug, we need to properly handle the `Popen` object by closing it after reading the output. This will ensure that the output is read correctly without any extra information included.

## The corrected version of the function

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    proc.stdout.close()  # Close the stdout to prevent reading additional data
    return u'Fish Shell {}'.format(version.replace('fish, version ', ''))
```

By adding `proc.stdout.close()` after reading the output, we ensure that only the necessary version information is extracted. Additionally, we modify the return statement to exclude the unnecessary part of the output string.

This corrected version of the function should now pass the failing test and provide the expected output.