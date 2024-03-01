### Bug Explanation

The bug in the `_dict_arg` function lies in how it generates the command list. When iterating over the dictionary items, the function is incorrectly adding double quotes around the property value pair, resulting in a mismatch with the expected output.

In Case 1, the expected output for the `--conf` argument is `'--conf', 'Prop=Value'`, without the double quotes around the `Value`. However, the function is returning `['--conf', '"Prop=Value"']`, causing the test to fail.

Similarly, in Case 2, the expected output for the `--conf` argument is `'--conf', 'prop1=val1'`, without the double quotes around the `val1`. But the function is returning `['--conf', '"prop1=val1"']`, leading to the test failure.

### Bug Fix Strategy

To fix this bug, we need to modify the `_dict_arg` function to correctly generate the command list without including unnecessary double quotes around the property value pairs.

### Corrected Version

```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
```

By using `'{0}={1}'.format(prop, val)` we can correctly build the command list without adding unnecessary double quotes. This corrected version should pass the failing tests.