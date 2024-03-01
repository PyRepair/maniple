### Analysis:
1. The `table_exists` function in the `HiveCommandClient` class checks if a table exists in a database using hive invocations.
2. The bug is related to case sensitivity when comparing table names.
3. The bug arises because the function does a direct string comparison without considering case sensitivity, causing failures when table names have different cases.
4. To fix the bug, we need to ensure the comparison between the table name and the output from `run_hive_cmd` is case insensitive.

### Bug Fix Strategy:
1. Update the comparison logic to convert both the table name and the output to lowercase before comparison.
2. Modify the return statements to compare lowercase versions of the table name and the stdout.

### Corrected Version:
```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

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

By converting both the table name and the stdout to lowercase before comparison, the corrected function ensures that the check for table existence is case insensitive, addressing the bug reported in the GitHub issue.