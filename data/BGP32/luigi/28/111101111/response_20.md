To fix the bug in the `table_exists` function to make it case insensitive, we need to modify the comparison between the table name and the output from Hive to ensure it works correctly with any casing. By converting both the table name and the output to lowercase before comparison, we can address the issue.

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

By converting both the table name and the output to lowercase before comparison, the function will now be case insensitive and pass the failing test cases.

This approach aligns with the suggestion in the GitHub issue #896 to make the `table_exists` function case insensitive in its comparison, addressing the specific problem described.