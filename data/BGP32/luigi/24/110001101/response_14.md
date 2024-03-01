### Bug Explanation
The bug in the `_dict_arg` function arises from adding unnecessary double quotes around the key-value pairs in the command list. This results in the incorrect format of the command list when the function returns, which causes the tests to fail.

### Fix Strategy
To fix this bug, we need to remove the unnecessary double quotes around the key-value pairs in the command list.

### Corrected Version
```python
class SparkSubmitTask(luigi.Task):
    def _dict_arg(self, name, value):
        command = []
        if value and isinstance(value, dict):
            for prop, val in value.items():
                command += [name, '{0}={1}'.format(prop, val)]
        return command
``` 

Now, the corrected `dict_arg` function will generate the command list with the correct format without unnecessary double quotes, meeting the expected input/output values.