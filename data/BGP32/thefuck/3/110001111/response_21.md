### Analysis
1. The buggy function `info` in the `Fish` class is attempting to retrieve the version of the Fish shell by executing a command in the shell.
2. The function uses the `Popen` class to execute the command `'fish -c echo $FISH_VERSION'`, but the retrieval of the version seems to be incorrect based on the provided runtime values.
3. The `expected` output version value is `'3.5.9'`, which is different from the actual `version` value `'fish, version 3.5.9'`. This discrepancy is likely causing the bug.
4. The GitHub issue mentions a recursive loop issue triggered by the use of `-v` option, which implies there might be a problem with how the version is being retrieved.
5. A strategy to fix the bug would involve modifying how the version is extracted from the output of the command.

### Bug Fix
Here is a corrected version of the `info` function in the `Fish` class:

```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()

        # Fix the version extraction by splitting the output
        version_parts = version.split(',')
        if len(version_parts) > 1:
            version = version_parts[1].strip()

        return u'Fish Shell {}'.format(version)
```

This fix involves splitting the retrieved `version` string by a comma to extract the actual version number from the output. This modification should correctly parse the version and prevent the bug that caused the incorrect version.