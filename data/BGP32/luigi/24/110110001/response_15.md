## Bug Analysis:
1. The buggy function `_dict_arg` within the `SparkSubmitTask` class in `luigi/contrib/spark.py` is expected to convert a dictionary argument into a list of command arguments. However, there is a bug in how the key-value pairs are being formatted into the command arguments.
2. The bug occurs when converting the dictionary entries into command arguments, where the value is enclosed within double quotes, causing incorrect assertion failures in the test cases.

## Bug Explanation:
1. In the failing test cases, the assertion error is due to the incorrect formatting of key-value pairs from the dictionary. The expected format is `'--conf', 'prop1=val1'` but the buggy function outputs `'--conf', '"prop1=val1"'`.
2. This issue arises from the buggy function including double quotes around the value while constructing the command list. This leads to a mismatch in the expected and actual command arguments when comparing in the test cases.

## Bug Fix:
To fix this bug, we need to ensure that the values from the dictionary are included in the command list without being enclosed in double quotes. We can achieve this by removing the unnecessary double quotes around the formatted key-value pairs.

## Fixed Version of the `_dict_arg` Function:
```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
```

By removing the unnecessary double quotes in the command construction, the bug should be resolved, and the corrected function should pass the failing test cases without assertion errors.