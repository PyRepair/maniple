### Bug Explanation
The bug in the `table_exists` function stems from the incorrect condition check when determining if a table exists in the database. In the `if` block where `partition is None`, the function checks if the `table` is in the `stdout` output from running a Hive command. However, the condition is flawed as it only checks if `stdout` exists and the table name is in it, regardless of whether the output is actually related to table existence.

### Bug Fix Strategy
To fix the bug, we need to ensure that the function correctly identifies if a table exists in the database based on the output of the Hive command. We should modify the condition check to properly evaluate whether the table is present in the output for both the cases when `partition` is `None` and when it is not `None`.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and table in stdout.splitlines()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By splitting the `stdout` output into lines before checking for table existence, we ensure that the function accurately identifies if the table exists. The corrected function should now pass the failing tests and meet the expected input/output values.