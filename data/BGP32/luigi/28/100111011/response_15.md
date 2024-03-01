The bug in the `table_exists` function lies in the comparison between the table name and the output from the Hive command. The comparison is case-sensitive, leading to test failures when the table names do not match exactly. The fix involves converting both the table name and the output to a consistent case for comparison.

### Bug Cause:
The buggy function does not transform the table name to a consistent case when comparing with the output from the Hive command. This leads to case-sensitive comparisons causing test failures.

### Fix Strategy:
1. Convert the `table` variable to lowercase before comparing it with the stdout for case-insensitive matching.
2. Check if the lowercase version of the `table` exists in the lowercase version of the `stdout` to ensure case insensitivity.

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

By making this change, the function will now perform case-insensitive comparison between the table name and the Hive output, resolving the test failures reported in the GitHub issue.