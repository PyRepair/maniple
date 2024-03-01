### Bug Explanation
The bug in the provided function lies in the condition checking for the existence of the table. In the first case, the function checks if the table name exists within the output of the `show tables` command. However, this check is case-sensitive, leading to incorrect results in Case 2 when the table name has a different case than expected.

### Bug Fix Strategy
To fix the bug, we need to make the table name comparison case-insensitive. This can be achieved by converting both the table name and the output to a consistent case (usually lowercase) before comparison.

### Corrected Code
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