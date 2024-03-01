### Analysis and Explanation:
The buggy function `table_exists` has several issues:
1. In the case where `partition` is `None`, the function is running the command to check if the table exists in the specified database. However, the condition `stdout and table in stdout` is incorrect because the `run_hive_cmd` function does not return a boolean value. It should instead check if the table name is present in the `stdout` string.
2. In the case where `partition` is not `None`, the function is running a command to check if the partitions exist for the specified table. The condition `if stdout` is not enough to determine if the partitions exist, as the command output may contain other information. It should instead check if the specified partition is in the `stdout` string.

### Bug Fix Strategy:
1. Update the condition in the first case to check if the `table` name is present in the `stdout` string.
2. Update the condition in the second case to check if the specified `partition` is in the `stdout` string.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return partition in stdout
```