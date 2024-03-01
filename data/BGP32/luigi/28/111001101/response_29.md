The bug in the `table_exists` function is related to how the `stdout` variable is being used to check if the table exists in the database. The bug arises because the function checks if the table name is directly present in the `stdout` output, which can lead to false positives if the table name is part of a larger string in the output.

To fix this bug, we should modify the logic to check for exact matches of the table name within the `stdout` output.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables in {1}'.format(database, table))
    
        return stdout and table in stdout.splitlines()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
    
        return bool(stdout)
```

In this corrected version:
- We use the `in` operator along with `splitlines()` to check if the table name exists exactly in the `stdout` output.
- For the case where checking for partitions, we return `bool(stdout)` directly, as we only need to check if `stdout` contains any partitions.

This correction should now correctly determine if the table exists in the database based on exact matches in the output.