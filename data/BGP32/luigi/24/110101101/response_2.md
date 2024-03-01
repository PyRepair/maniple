#### Bug Explanation
The bug in the `_dict_arg` function is caused by the way the command list is constructed. The current implementation is adding extra quotations around the key-value pairs when creating the command list, which causes the test cases to fail.

In the failing test cases provided:
- The expected command list should not have quotation marks around the key-value pairs.
- The key-value pairs should be formed directly without extra formatting.

#### Bug Fix Strategy
To fix the bug, we should modify the `_dict_arg` function to create the command list without adding extra quotations around the key-value pairs. Instead, we should directly append the key-value pairs to the command list in the correct format.

#### Corrected Version
```python
class SparkSubmitTask(luigi.Task):
    def _dict_arg(self, name, value):
        command = []
        if value and isinstance(value, dict):
            for prop, val in value.items():
                command += [name, '{0}={1}'.format(prop, val)]  # Correct the format of key-value pairs
        return command
``` 

With this corrected version, the function should now generate the command list properly without extra quotations, and the failing test cases should pass.