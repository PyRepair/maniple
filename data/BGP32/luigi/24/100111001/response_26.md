### Bug Explanation
The bug in the `_dict_arg` function occurs due to the incorrect formatting of key-value pairs when constructing the command list. The current implementation surrounds the property value with double quotes which is causing the `AssertionError` in the test cases as the expected values do not have the double quotes.

### Bug Fix Strategy
To fix the bug, we need to modify the way key-value pairs are formatted when constructing the command list. Instead of including double quotes around the property values, we should directly concatenate the property and value without quotes.

### Corrected Version
```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
``` 

### Updated Runtime Values
After applying the corrected version of the function, the runtime values should be:
#### Case 1
- command: `['--conf', 'Prop=Value']`
- value: `'Value'`
- prop: `'Prop'`

#### Case 2
- command: `['--conf', 'prop1=val1']`
- value: `'val1'`
- prop: `'prop1'` 

By making these changes, the function will correctly format the key-value pairs in the command list, leading to passing test cases without any `AssertionError`.