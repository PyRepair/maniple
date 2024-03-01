The bug in the provided function `info` lies in how the version information is retrieved from the `Popen` process. The bug causes the output to include unwanted text "Fish Shell" along with the actual version number. This causes unexpected behavior when trying to determine the shell version.

Based on the GitHub issue, the bug triggers a recursive loop because the version information contains extra text that is not expected in the output. To fix this bug, we need to modify the way we extract the version number from the output of the `Popen` process.

### Bug Explanation:
In the buggy function `info`, the `Popen` process is used to execute the command `'fish -c echo $FISH_VERSION'` to get the version of the Fish shell. However, the obtained output includes the text "Fish Shell" along with the version number which causes incorrect behavior and may lead to infinite recursive loops as reported in the GitHub issue.

### Fix Strategy:
To fix the bug, we need to modify the way we extract the version number from the output. We can simply split the obtained version string based on commas and extract the second part containing only the version number. This will ensure that only the version number is returned without any unwanted text.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', version ')[-1]
        return version
```

With this corrected version of the `info` function, the function will extract only the version number from the output of the `Popen` process. This change ensures that the function returns the correct version of the Fish shell without any extra text, addressing the bug and potential recursive loop issue reported in the GitHub.