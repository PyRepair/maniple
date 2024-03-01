### Bug Explanation
The bug in the `table_exists` function is that it incorrectly checks if the table exists in the stdout output. In the initial implementation, the function returns true only if the table name is an exact match with the stdout, which is not always the case. The correct behavior should be to check if the table name appears in a line within the stdout.

### Bug Fix Strategy
1. We need to split the stdout into lines.
2. Check if any line contains the table name.
3. Return true if the table name is found in any line.

### Corrected Version of the Function
```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            stdout_lines = stdout.split('\n')
            return any(table in line for line in stdout_lines)
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
            return bool(stdout)
```

With these changes, the `table_exists` function should now correctly check for the existence of the table in the stdout output, as expected by the test cases.