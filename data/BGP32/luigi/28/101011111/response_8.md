The bug in the `table_exists` function is due to a case sensitivity issue. The function compares the table name with the output of the Hive command without considering the case of the characters. To fix this bug, we need to convert both the table name and the output to lowercase before comparison.

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

By converting both the table name and the stdout to lowercase during comparison, the function will now be case insensitive, as requested in the GitHub issue. This change will ensure that the tests pass and that the function behaves correctly with regards to case sensitivity.