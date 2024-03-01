### Bug Analysis:
1. The `table_exists` function in `hive.py` is not handling the case sensitivity of table names, leading to failing test cases.
2. The failing tests indicate that the function is not returning the correct values when checking for table existence due to case sensitivity issues.
3. The expected values are not being met because the function does not account for differences in case when comparing table names in the `stdout`.
4. To fix the bug, we need to modify the function to convert both the table name and `stdout` to lowercase before comparison.

### Bug Fix:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table.lower()))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table.lower(), self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By converting both the `table` and `stdout` to lowercase during comparison, the function now properly handles case sensitivity issues related to table names. This fix aligns with the GitHub issue raised and the suggested solution to make the `table_exists` function case insensitive.