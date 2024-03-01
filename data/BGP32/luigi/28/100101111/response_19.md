### Explanation:
The bug in the `table_exists` function is that it does not handle case insensitivity when comparing the table name in the `stdout` with the provided table name. As a result, the function fails to correctly determine if a table exists when considering different cases of table names.

### Strategy for Fixing the Bug:
To fix the bug, we need to ensure that we convert both the table name provided as input and the table names in the `stdout` to a consistent case (e.g., lower case) for comparison. This modification will make the function case insensitive when checking if a table exists.

### Corrected Version of the Function:
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

By implementing the changes in the corrected version of the function above, the function now performs a case-insensitive check when determining if a table exists. This fix aligns with the reported issue in GitHub and addresses the problem effectively.