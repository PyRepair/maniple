### Bug Explanation
The bug in the `table_exists` function lies in the comparison of the `table` string with the `stdout` variable. In the case where the `table` names have different cases (e.g., "mytable" and "MyTable"), the function fails to correctly identify the table exists due to case sensitivity.

### Bug Fix Strategy
To fix the bug, we need to ensure that the comparison between the `table` name and the table names in `stdout` is case-insensitive.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        tables = stdout.strip().split('\n')
        
        return any(t.lower() == table.lower() for t in tables)
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

In this corrected version, we split the `stdout` by newline characters to get a list of table names and then use `any()` to check if any table name matches the input `table` string regardless of case. This ensures a case-insensitive comparison.