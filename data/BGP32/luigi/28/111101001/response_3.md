### Bug Explanation
The bug in the `table_exists` function lies in the comparison condition for checking if the table exists in the output from the `run_hive_cmd` function. The current implementation checks if the `table` is in the `stdout` output directly, but the comparison fails in certain cases due to extra characters in the output or case sensitivity issues.

### Bug Fix Strategy
To fix the bug, we should modify the comparison part to handle cases where there might be extra characters in the output or case sensitivity issues. One approach could be to split the `stdout` by newline characters and then check if the `table` matches any line. Additionally, we should consider case insensitivity when comparing the table names.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        if stdout:
            return any(t.lower() == table.lower() for t in stdout.split('\n'))
        else:
            return False
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By modifying the comparison logic to check each line in the `stdout` after splitting by newline characters and converting both table names to lowercase for a case-insensitive comparison, the corrected function should now pass the failing test cases.