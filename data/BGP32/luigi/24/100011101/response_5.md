The issue in the provided function is due to the extra double quotes added around the property=value pair when creating the command list.

### Bug Explanation:
1. In Case 1, the expected output should be `['--conf', 'Prop=Value']` with the property and value pairs correctly formatted without extra quotes. However, the actual output contains extra quotes around the property=value pair, causing a mismatch.
   
2. In Case 2, the expected output should be `['--conf', 'prop1=val1']` with the property and value pairs correctly formatted without extra quotes. But the actual output has extra quotes around the property=value pair, leading to a failing assertion.

### Fix Strategy:
To fix the bug, we need to remove the extra quotes that are added around the property=value pair when constructing the command list.

### Corrected Function:
```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, "{0}={1}".format(prop, val)]
    return command
```

By using string formatting directly without enclosing the property=value pair in extra quotes, we can ensure that the command list is correctly generated without the additional quoting issue.