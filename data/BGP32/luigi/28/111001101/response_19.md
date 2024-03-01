### Bug Explanation
The bug in the `table_exists` function occurs due to the comparison of the `table` name with the `stdout` string. The function checks if the `table` name is within the `stdout` string, but because it doesn't properly handle the case sensitivity of the table names, it sometimes fails to find a match even when the table exists. This results in incorrect output.

### Bug Fix Strategy
To fix the bug, we should make the comparison case-insensitive so that it can correctly identify the existence of the table despite the case variation in the input parameters.

### Corrected Version of the function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and any(t.lower() == table.lower() for t in stdout.split())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

This corrected version compares the lowercase version of the table names in both the `table` variable and the `stdout` string to ensure a case-insensitive comparison. This modification will improve the accuracy of the `table_exists` function in detecting if a table exists in the specified database.