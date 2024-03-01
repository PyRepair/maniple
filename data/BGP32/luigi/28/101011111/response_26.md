To fix the bug in the `table_exists` function, we need to address the case sensitivity issue when comparing the table name with the output from the Hive command. The comparison should be case insensitive to handle scenarios where the table names have different casing.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
    
        if stdout:
            return True
        else:
            return False
```

In the corrected version:
- We convert both the `table` and `stdout` to lowercase before comparison to make it case insensitive.
- This change ensures that the function correctly identifies the table existence regardless of the casing of the table name.

By implementing this fix, the function should now pass the failing test cases provided and satisfy the expected input/output values. This will also address the case sensitivity issue mentioned in the GitHub issue #896.