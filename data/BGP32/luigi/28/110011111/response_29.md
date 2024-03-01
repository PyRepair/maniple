### Identified Bug:
The bug in the `table_exists` function is that the comparison between the table name and the output from the `run_hive_cmd` function is case-sensitive. Since Hive is case-insensitive when it comes to table names, this leads to test failures when the case of the table name does not match the case of the output from Hive.

### Fix Strategy:
To fix the bug, we need to perform a case-insensitive comparison between the table name and the output from `run_hive_cmd` in the `table_exists` function.

### Correction:
Here is the corrected version of the `table_exists` function:

```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """


    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

            return stdout and table.lower() in map(str.lower, stdout.splitlines())
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

            if stdout:
                return True
            else:
                return False
```

### Explanation:
In the corrected version, the comparison `table.lower() in map(str.lower, stdout.splitlines())` ensures that the comparison is case-insensitive by converting both the table name and the lines from the `stdout` to lowercase before checking for the presence of the table name.

With this correction, the function will now correctly handle case-insensitive comparisons when checking for the existence of a table in Hive, addressing the issue reported on GitHub.