To fix the bug in the `table_exists` method, we need to make the comparison between the table name and the tables listed in the `stdout` case-insensitive. This will ensure that the method detects the table correctly regardless of the case.

Here is the corrected version of the `table_exists` method:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

By changing the comparison to be case-insensitive (`table.lower() in stdout.lower()`), the method will correctly identify the table in the `stdout` output even if the cases do not match.

This correction aligns with the suggested fix in GitHub issue #896, which addresses the case sensitivity issue in the `table_exists` method.