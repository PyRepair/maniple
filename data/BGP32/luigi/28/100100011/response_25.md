The bug in the `table_exists` function is due to case sensitivity when comparing the table name with the output from the hive command. The issue reported on GitHub suggests that tables defined with capitalized names may fail the test because the hive output returns lower case names.

To fix this bug, we need to ensure that the comparison is case insensitive by converting both the table name and the hive output to lowercase before checking for existence.

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

By converting both `table` and `stdout` to lowercase before comparison, the `table_exists` function will now pass the test cases, addressing the GitHub issue of making the function case insensitive.