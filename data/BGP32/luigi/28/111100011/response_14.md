The bug in the `table_exists` function is related to case sensitivity when checking for table existence in Hive. The bug causes the function to fail when comparing table names due to case differences.

To fix this bug:
- Modify the comparison in the `table_exists` function to check if the lowercase version of the table exists in the lowercase version of the stdout.
- Update the function to be case insensitive when checking for table existence.

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

With this modification, the `table_exists` function should now be case insensitive when checking for table existence in Hive. It should pass the failing test cases and resolve the issue reported on GitHub (#896).