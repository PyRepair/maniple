To fix the bug in the `table_exists` function, we need to make the comparison case insensitive by converting both the table name and the stdout result to a consistent case before comparison. 

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

Explanation:
- In the corrected version, both the `table` name and the `stdout` result are converted to lowercase using the `lower()` method before comparison. This ensures that the comparison is case insensitive. 
- By making the comparison case insensitive, we address the issue raised in the GitHub discussion (#896) about table names being returned in lowercase by Hive.
- The corrected function should now pass the failing test cases by correctly handling the case sensitivity of table names in the output from Hive.