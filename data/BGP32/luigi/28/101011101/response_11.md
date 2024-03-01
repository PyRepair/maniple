### Bug Explanation
The bug in the `table_exists` function arises from the condition checking when `partition` is not None. The function correctly composes the Hive command, but the condition `if stdout:` does not handle the case where the table actually exists in the result of the `run_hive_cmd`. This leads to incorrect return values and failing tests.

### Bug Fix Strategy
To fix the bug, we need to modify the condition in the `else` block where we check if `table` is in the `stdout`. Instead of simply checking for the truthiness of `stdout`, we should explicitly check if `table` is in the `stdout` string. This way, we can accurately determine if the table exists.

### Corrected Code
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return table in stdout
``` 

By modifying the return statement in the `else` block to directly check if `table` is in `stdout`, we can ensure that the function correctly determines if the table exists in the specified conditions. This corrected version should pass the failing tests.