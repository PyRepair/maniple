The issue with the function `table_exists` is that it does not handle case sensitivity properly when checking for the existence of tables in Hive. This leads to failures when the table names are provided with different cases (e.g., 'MyTable', 'mytable').

To fix this issue, we need to modify the comparison between the table name and the table names returned by Hive in a case-insensitive manner.

Here is the corrected version of the function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in map(str.lower, stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

In this corrected version, we use `table.lower()` and `map(str.lower, stdout.split('\n'))` to perform a case-insensitive comparison between the table names. This ensures that the function works correctly when dealing with tables that have different cases.

By making this change, we address the issue described in the GitHub post and provide a more robust implementation of the `table_exists` function.