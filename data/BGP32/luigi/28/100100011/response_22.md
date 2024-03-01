### Explanation:
The bug in the `table_exists` function arises from the case sensitivity of table names in Hive. The function checks for the existence of a table by directly comparing the table name with the output from Hive, which may cause issues due to case differences in the names. The failing test case for `table_exists` in `hive_test.py` demonstrates this problem by showing that tables with different cases are not identified correctly.

### Solution Strategy:
To fix this bug and make the `table_exists` function case insensitive, we need to modify the comparison between the table name and the output from Hive. One approach is to convert both the table name and the output to lowercase before comparing them. This way, case differences will not affect the result of the check.

### Corrected Version of the `table_exists` function:
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

By making this change, the `table_exists` function will compare table names in a case-insensitive manner, allowing it to correctly identify table existence regardless of case differences in the names. This corrected version should pass the failing test case and resolve the issue reported on GitHub.