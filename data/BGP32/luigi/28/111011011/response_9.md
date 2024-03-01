### Identified Bug:
The bug in the `table_exists` function is due to it not being case insensitive when comparing the table name with the output from the `run_hive_cmd` function. This causes the test cases to fail when table names are provided in different cases than what is returned by Hive.

### Fix Strategy:
To fix the bug, we need to ensure that the comparison between the table name and the output from `run_hive_cmd` is case insensitive. By converting both the table name and the output to lowercase before comparison, we can address the issue reported in the GitHub ticket.

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

### Updated Function Explanation:
The corrected version of the `table_exists` function now converts both the `table` name and the `stdout` output to lowercase before performing the comparison. This change makes the comparison case insensitive and resolves the issue reported in the GitHub ticket.

By using `table.lower() in stdout.lower()` in the return statements, the function will now correctly identify the existence of a table regardless of the case in which it is provided.

This fix ensures that the function behaves as expected and passes the failing test cases.