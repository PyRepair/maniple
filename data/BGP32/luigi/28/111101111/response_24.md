To fix the bug in the `table_exists` function, we need to address the case sensitivity issue when checking for table existence. The function should compare the table name in a case-insensitive manner. Here is the corrected version of the function:

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

By modifying the comparison to be case-insensitive (`table.lower() in stdout.lower()`), the function will correctly identify the existence of the table regardless of the case used in the input. This change aligns with the solution proposed in GitHub issue #896 to address the case sensitivity issue.