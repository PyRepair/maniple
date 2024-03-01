Based on the information provided, the bug in the `info` function of the `Fish` class is caused by the incorrect command used to retrieve the Fish shell version. The `echo $FISH_VERSION` command does not accurately provide the version number, resulting in the failing test.

Here is a corrected version of the `info` function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version_info = version.split()[-1]
        return f'Fish Shell {version_info}'
```

With this correction, the function uses the correct command `['fish', '--version']` to retrieve the Fish shell version. It then extracts the version number from the output and returns it as `'Fish Shell {version}'`.

This correction should resolve the failing test case and address the issue raised on GitHub regarding the recursive loop triggered by the incorrect version retrieval method.