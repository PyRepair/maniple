### Bug Explanation:
The bug in the `table_exists` function is due to the check on whether the table name exists in the stdout. The condition `return stdout and table in stdout` is checking if both conditions are true, which is incorrect. Instead, it should check if `table` is in `stdout`. 

### Bug Fix Strategy:
1. Modify the condition `return stdout and table in stdout` to `return table in stdout`.
2. Ensure that the function handles case insensitivity when comparing the table names.

### Corrected Function:
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