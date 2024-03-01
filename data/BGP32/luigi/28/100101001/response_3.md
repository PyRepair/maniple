### Bug Analysis:
The bug in the `table_exists` function seems to be related to how the stdout output is being checked to determine if the table exists. The function is currently checking if the entire `table` name is in the `stdout` string, which may not work correctly in all cases (as seen in the failing tests).

### Bug Explanation:
In the failing test cases provided:
1. In Case 1 and Case 3, the `table_exists` function is returning False even when the table name exists in the stdout output. This is because the function is checking for an exact match of the `table` name in the `stdout` string, which is not the correct approach.
2. In Case 2 and Case 4, the function is returning True when the table name exists in the stdout output. This indicates that the current implementation is inconsistent and needs to be fixed.

### Bug Fix Strategy:
To fix the bug, we need to modify the logic for checking whether the table exists in the `stdout` output. Instead of checking for an exact match, we can improve the logic to search for the table name within the `stdout` string by splitting the `stdout` on newlines and checking if the table name is present in any of the lines.

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and any(table in line for line in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

By implementing this corrected version, the function should now properly check if the table name exists in the `stdout` output and return the correct result based on that.