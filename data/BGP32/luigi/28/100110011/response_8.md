The bug in the `table_exists` function arises from the fact that the comparison between the table name and the output from the Hive command is case sensitive. As mentioned in the GitHub issue, Hive is case insensitive, so the comparison should be made ignoring the case of the characters. 

To fix the bug:
1. Adjust the comparison between the table name and the output from the Hive command to be case insensitive.
2. Ensure that the correct table name is being compared against the output from the Hive command.

Here is a corrected version of the `table_exists` function:

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

By making the comparison case insensitive by converting both the table name and the output from the Hive command to lowercase, the function should now pass the failing test cases and resolve the issue reported on GitHub.