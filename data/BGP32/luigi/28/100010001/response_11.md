The bug in the `table_exists` function is related to how the function is checking for the presence of a table in the database. The function is expecting the output of the `run_hive_cmd` function to be the literal table name, but in the failing test cases, the output includes more information (e.g., "OK\nmytable"). This discrepancy causes the function to incorrectly determine whether the table exists.

To fix this bug, we can modify the function to correctly process the output of `run_hive_cmd` and extract the table name for comparison.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        tables = stdout.strip().split('\n')
        return table in tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
```

In the corrected version:
1. We split the output of `run_hive_cmd` by newline character `\n` to get a list of table names when checking for table existence.
2. We use `strip()` to remove leading and trailing whitespace from the output.
3. When checking the table existence after querying the partitions, we simply return a boolean based on whether the `stdout` is empty or not.

With these modifications, the function should now correctly determine whether a table exists in the database.