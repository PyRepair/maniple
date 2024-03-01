## Analysis
1. The buggy function `info` in the `Fish` class is supposed to return the name and version of the current shell (Fish shell). It uses the `Popen` function to execute a command to get the version of Fish shell.
2. The error is due to the fact that the version retrieved from the command includes unnecessary text "fish, version" before the actual version number. This discrepancy causes the assertion error.
3. The expected version value is `'3.5.9'`, but the actual version value retrieved includes the text `'fish, version'`.
4. To fix the bug, we need to modify the extraction of the version number from the command output to only include the version number itself without any additional text.

## Bug Fix Strategy
Since the version number itself is what we need and not any additional text, we can modify the way we extract the version from the command output. We can split the output based on the comma (`,`) and get the second part, which should be the actual version number without any additional text.

Let's correct the function based on the analysis and bug fix strategy.

## Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
        return u'Fish Shell {}'.format(version)
```

By splitting the version number using `split(',')`, we can obtain the version number without any additional text. This corrected version should now correctly extract the version number and pass the failing test.