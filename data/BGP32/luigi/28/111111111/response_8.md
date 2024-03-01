Fixed and corrected version of the buggy function:

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

This corrected version uses case-insensitive comparisons by converting both the table and stdout to lowercase before checking if the table exists in the hive output. This change addresses the issue described in the GitHub report by making the `table_exists` function case-insensitive.