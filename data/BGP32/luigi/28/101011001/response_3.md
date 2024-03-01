### Bug Explanation:
The bug in the `table_exists` function is that it checks for the presence of the table name in the output of the `run_hive_cmd` function without considering the case sensitivity of the table names. This causes the function to return incorrect results when the case of the table name does not match exactly with the case in the output.

### Bug Fix Strategy:
To fix this bug, we need to make the comparison case-insensitive. This can be achieved by converting both the table name and the table names from the `run_hive_cmd` output to lowercase before comparison.

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

With this correction, the function will now compare the table names in a case-insensitive manner, making the tests pass correctly.