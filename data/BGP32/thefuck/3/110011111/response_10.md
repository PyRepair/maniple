## Bug Explanation

The bug in the `Fish.info` function arises from the fact that the `version` variable is assigned the entire output including the text "fish, version". When the function constructs the return value, it includes this extra text causing the assertion to fail.

## Fix Strategy

To fix this bug, we need to extract only the version number from the `version` variable before constructing the return string.

## The corrected version of the function

```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(" ")[-1]
        return u'Fish Shell {}'.format(version)
```

By splitting the version string based on spaces and selecting the last part, we ensure that only the version number gets included in the return value. This corrected version should pass the failing test and satisfy the expected input/output values.