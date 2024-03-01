The issue with the `table_exists` function is that it checks for the presence of the table name in the output of the `run_hive_cmd` function without considering the formatting of the output. The `run_hive_cmd` function might return additional data along with the table name, causing the presence check to fail.

To fix this issue, a better approach would be to split the output of `run_hive_cmd` by newlines and then check if the table name is present in any of the lines.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

This corrected version splits the output of `run_hive_cmd` by newlines before performing the table name check. This approach ensures that the table name presence is accurately verified, considering possible additional output in the stdout.

By using this corrected version, the failing tests should pass as expected.