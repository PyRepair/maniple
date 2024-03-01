### Bug Analysis:
1. The `table_exists` function is failing the test cases due to case sensitivity when comparing the table name from stdout with the input table name.
2. The function does not handle case sensitivity properly, leading to incorrect results when comparing the table names.
3. The failing test cases show that the function expects the comparison to be case insensitive, but the function currently performs a direct comparison which fails in case of different cases.
4. The suggested fix is to convert both the input table name and the table name from stdout to lowercase before comparison.

### Bug Fix:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By converting both the input table name `table` and the table name from `stdout` to lowercase before comparison, the function will now be case insensitive and pass the failing test cases.