### Bug Analysis
1. The buggy function `_dict_arg` is designed to construct a command list based on key-value pairs in a dictionary.
2. The bug occurs when constructing the command list by adding the key-value pairs as separate elements instead of combining them as a single string.
3. When constructing the command list, for key-value pairs like `'"Prop=Value"'`, the expected output should be `'--conf', 'Prop=Value'` but the function is providing `'"Prop=Value"'`.
4. The bug results in a type mismatch and extra characters in the constructed command list.

### Bug Fix Strategy
To fix the bug in the `_dict_arg` function:
1. Concatenate the key and value strings with an equal sign between them.
2. Implement this concatenation inside the loop where key-value pairs are processed.
3. Add the concatenated string as a single element to the `command` list.

### Corrected Version
```python
class SparkSubmitTask(luigi.Task):
    def _dict_arg(self, name, value):
        command = []
        if value and isinstance(value, dict):
            for prop, value in value.items():
                command += [name, '{0}={1}'.format(prop, value)]
        return command
```