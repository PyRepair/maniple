To fix the bug in the `table_exists` function, we need to make the comparison case-insensitive. The issue arises because the function is comparing the table name directly with the output from Hive, which may be in a different case. 

To resolve this, we should convert both the table name and the output to lowercase before comparing them. This will ensure that the comparison is case-insensitive and will prevent the test failures.

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

By converting both the table name and the stdout to lowercase using the `lower()` method, we ensure that the comparison is case-insensitive. This modification addresses the test failures and makes the function behave as expected based on the provided test cases and the GitHub issue description.