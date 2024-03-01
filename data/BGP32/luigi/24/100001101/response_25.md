The bug in the provided function lies in the way the values are concatenated to the command list. The values are being enclosed in double quotes unnecessarily. 

A strategy to fix the bug would be to remove the double quotes around the values before appending them to the command list.

Here is the corrected version of the function:

```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
``` 

This corrected version removes the unnecessary double quotes around the property-value pairs when constructing the command list, which will now output the expected values according to the given test cases.