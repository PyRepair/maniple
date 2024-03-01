### Analysis:
1. The `table_exists` function is designed to check if a table exists in a Hive database, but it is failing to handle case sensitivity properly, leading to test failures.
2. The issue arises because the function compares the table name directly with the output from Hive, which can be in lowercase.
3. The failing tests show that when the table name has different case variations, the function fails to return the correct result even if the table exists.
4. The suggested strategy is to modify the comparison between the table name and the Hive output to be case insensitive by converting both to lowercase before comparison.

### Correction:
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

By converting both the table name and the Hive output to lowercase before comparison, the corrected function will now handle case sensitivity properly. This adjustment aligns with the GitHub issue's suggestion to make the `table_exists` function case insensitive.