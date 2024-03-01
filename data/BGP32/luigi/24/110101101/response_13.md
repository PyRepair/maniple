### Bug Explanation
The bug in the `_dict_arg` function lies in the way the command list is constructed when value is a dictionary. The current implementation wraps the key-value pairs in quotes, which is unnecessary and causes the test to fail because the expected output does not have the key-value pairs quoted.

### Fix Strategy
To fix the bug, we need to remove the unnecessary quotes around the key-value pairs when constructing the command list. We should construct the command list with the format `'--key=value'`.

### Corrected Version
```python
class SparkSubmitTask(luigi.Task):
    def _dict_arg(self, name, value):
        command = []
        if value and isinstance(value, dict):
            for prop, val in value.items():
                command += [name, "--{0}={1}".format(prop, val)]
        return command
```

With this corrected implementation, the function should now properly generate the command list without quoting the key-value pairs, matching the expected output values in the failing tests.