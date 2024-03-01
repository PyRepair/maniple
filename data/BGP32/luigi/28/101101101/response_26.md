The bug in the `table_exists` function is due to the incorrect comparison of the table name with the output of the `run_hive_cmd` function. The function checks if the table name is a substring of the output, rather than an exact match.

To fix the bug, we need to modify the comparison logic to check for an exact match of the table name in the output. Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split("\n")
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

By splitting the stdout on newline characters, we can check for an exact match of the table name in the list of tables returned by the `show tables` command.

With this correction, the `table_exists` function should now pass the failing test cases provided.