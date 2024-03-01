The bug in the `_dict_arg` function lies in how it handles dictionary values. Currently, the function incorrectly wraps the property value pairs in double-quotes, leading to discrepancies with the expected output.

The strategy to fix this bug is to not enclose the property value pairs in double-quotes when constructing the command list.

Here is the corrected version of the `_dict_arg` function:

```python
# The relative path of the corrected file: luigi/contrib/spark.py

def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, prop_value in value.items():
            command += [name, '{0}={1}'.format(prop, prop_value)]
    return command
```

By making this change, the function will construct the command list correctly without unnecessary double-quotes.

This corrected version should now pass both failing tests with the expected outputs correctly constructed.