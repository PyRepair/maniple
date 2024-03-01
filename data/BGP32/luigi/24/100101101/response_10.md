## Bug Explanation
The bug in the `_dict_arg` function stems from the fact that the values being added to the `command` list are being enclosed in double quotes unnecessarily. This causes the command list to have extra quotes around the values which leads to a mismatch when compared to the expected values in the test cases.

## Bug Fix Strategy
To fix this bug, we need to modify the way values are added to the `command` list in the `_dict_arg` function. Instead of adding the values with double quotes, we should directly append the values without quotes to make sure they match the expected values in the test cases.

## Corrected Version of the `_dict_arg` function
```python
# The relative path of the buggy file: luigi/contrib/spark.py

# this is the corrected function
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, "{0}={1}".format(prop, val)]
    return command
```

By making this change, the corrected function will properly format the command list and the test cases mentioned in the description will pass successfully.