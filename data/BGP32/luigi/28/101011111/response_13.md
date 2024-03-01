The bug in the `table_exists` function is related to case sensitivity when comparing the table name from the command output. To fix this bug, we need to ensure that the comparison is case-insensitive by converting both the table name and the output to lower case before comparison.

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

This corrected version of the function ensures that both the `table` name and the `stdout` output are converted to lower case before comparison, making the function case-insensitive. This change should fix the failing test cases and address the issue reported on GitHub related to making the `table_exists` function case insensitive.