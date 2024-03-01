### Bug Explanation
The bug in the `table_exists` function lies in the condition checking whether the `table` exists in the `stdout` output from the Hive command. The function currently checks if the entire `table` string exists in the `stdout`, leading to issues with case sensitivity. This causes the test to fail when checking for a table with a different case, as the comparison is sensitive to the exact case of the table name in the output.

### Bug Fix
To fix the bug, we need to make the comparison case-insensitive. We can achieve this by converting both the `table` and the `stdout` strings to lowercase before comparing them. This way, the comparison will ignore the case of the strings and provide correct results.

### Corrected Version
```python
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

In the corrected version, we convert both the `table` and the lines in the `stdout` to lowercase using the `lower()` method. Additionally, we split the `stdout` by lines to handle multiple table outputs correctly. This modification ensures a case-insensitive comparison, addressing the bug and allowing the function to pass the failing tests.