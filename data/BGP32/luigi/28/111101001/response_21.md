The bug in the `table_exists` function lies in the condition checking for the table existence. The function checks if the table name is in the stdout, but it doesn't consider the case sensitivity of the table name.

To fix the bug, we need to make the comparison case-insensitive. We can achieve this by converting both the table name and the stdout to lowercase before comparison.

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

By comparing the lowercase versions of the table name and the stdout, the function will now correctly identify the table existence in a case-insensitive manner.