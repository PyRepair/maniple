### Bug Explanation
The bug in the `table_exists` function arises from the condition `return stdout and table in stdout`. This condition will return `True` only if both `stderr` is not empty and the `table` is present in `stdout`. In the failing cases, the condition is evaluating to `False` when it should be `True`.

### Bug Fix Strategy
To fix this bug, we need to update the condition to check if the `table` is in `stdout` regardless of whether `stderr` is empty or not. This way, the function will correctly determine if the table exists in the database.

### Updated Buggy Function
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By updating the condition to only check if the `table` is in `stdout`, the function will now correctly determine the existence of the table. This fix should make the failing tests pass.