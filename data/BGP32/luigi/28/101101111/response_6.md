The bug in the `table_exists` function is due to case-sensitivity when comparing the table name extracted from the Hive command output. To fix this issue and make the comparison case-insensitive, we need to convert both the table name and the output to lowercase for comparison.

Here is the corrected version of the `table_exists` function:

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

By converting both the table name and the output to lowercase before comparison, the function will now correctly identify the table regardless of the case used.

This modification addresses the issue described in GitHub and aligns with the expected behavior specified in the test cases. It ensures that the function is case-insensitive when checking the existence of a table in Hive.