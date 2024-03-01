The bug in the `table_exists` function arises from a case sensitivity issue when checking if a table exists in Hive. The function currently checks if the table name is in the output from `run_hive_cmd` without converting the table name to lowercase, leading to failures when tables are defined with different case styles.

To fix this bug, we should compare the lowercase version of the table name with the lowercase output from `run_hive_cmd`. This modification will make the table existence check case insensitive, as requested in the GitHub issue.

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

By comparing the lowercase table name and stdout, the function will now correctly identify table existence regardless of case. This change aligns with the request in the GitHub issue to make the `table_exists` function case insensitive.