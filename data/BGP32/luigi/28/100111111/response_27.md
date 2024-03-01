### Bug Explanation:

The bug arises due to a case sensitivity issue in the `table_exists` function where the comparison between the table name and the output from Hive commands is case sensitive. The failing test cases fail because they expect case-insensitive behavior, but the function does not provide that.

### Bug Fix Strategy:

To fix the bug, the comparison between the table name and the output from Hive commands should be made case-insensitive. This can be achieved by converting both the table name and the output to lowercase before comparison.

### Corrected Version of the Function:

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

By making the comparison case-insensitive, the corrected function should now pass the failing test cases and provide the expected behavior of case insensitivity for table name comparisons.