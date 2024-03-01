## Bug Explanation
The bug in the `_dict_arg` function arises from incorrectly adding the key-value pairs from the input dictionary with quotes around the values. This leads to a mismatch between the expected and actual output lists, causing the test cases to fail.

In the first failing test, the input dictionary `{'Prop': 'Value'}` should be converted to `['--conf', 'Prop=Value']`. However, the function is returning `['--conf', '"Prop=Value"']`, including unnecessary double quotes around the value.

Similarly, in the second failing test, the input dictionary `{'prop1': 'val1'}` should result in `['--conf', 'prop1=val1']`, but the function is returning `['--conf', '"prop1=val1"']` with double quotes around the value.

## Fix Strategy
To fix this bug, we need to remove the unnecessary double quotes that are added around the property values. The keys and values should be concatenated without any additional characters in between.

## The Corrected Version of the Function
Here is the corrected version of the `_dict_arg` function:

```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
```

With this correction, the function will properly create the command list without any extra characters around the property values, addressing the issue causing the failing tests.