### Explanation of the bug
The bug is in the `table_exists` function of the `HiveCommandClient` class. The bug occurs when checking if a table exists in a given database. The function is intended to run a Hive command to check for the existence of the table, but the check is not correctly identifying the table in the output.

In the first condition (when `partition` is None), the function is checking if the `table` string is in the output from the Hive command. However, the comparison is not handling cases where the table name may appear within other text in the output.

In the second condition (when `partition` is not None), the function is attempting to check if the command output is not empty to determine the existence of the table. However, the condition is returning `True` regardless of the actual presence of the table.

### Bug fix strategy
To fix the bug, we need to modify the conditions for checking table existence. Instead of a simple string comparison, we should ensure that the table name appears as a separate entity in the output.

### Corrected version of the function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))

        tables = stdout.split()
        return table in tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

In the corrected version, we split the output by spaces to get individual table names in the first condition. Then, we check if the table name exists in the list of tables.

In the second condition, we directly return the boolean value of whether the command output is not empty.