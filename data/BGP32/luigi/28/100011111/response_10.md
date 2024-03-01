### Bug Analysis:
1. The `table_exists` function is failing tests due to case sensitivity issues when comparing table names against the output from Hive commands.
2. The failing tests expect the function to handle case insensitivity by comparing table names in a case-insensitive manner.
3. The bug causes the tests to fail when the table name case does not match the case of the table name in the Hive output.
4. The suggested fix is to make the comparison case insensitive by converting both the table name and the Hive output to lowercase before comparison.

### Bug Fix:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table)).lower()

        return stdout and table.lower() in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition))).lower()

        if stdout:
            return True
        else:
            return False
```

### Explanation:
1. The fixed function converts both the `stdout` and the `table` names to lowercase before comparison.
2. By making the comparison case insensitive, the function now correctly handles different cases of table names.
3. The fix addresses the issue reported on GitHub (#896) regarding making `table_exists` case insensitive.
4. The corrected function should pass the failing tests and satisfy the expected input/output values.