### Bug Analysis:
1. The `table_exists` function in the `HiveCommandClient` class does not handle case insensitivity when checking for the existence of a table.
2. The failing test cases expect the function to ignore case differences in table names.
3. The GitHub issue #896 highlights the need to make the `table_exists` function case insensitive to avoid failing tests due to case mismatches.

### Bug Fix Strategy:
To fix the bug, modify the `table_exists` function to compare the lowercase version of the table name with the lowercase version of the output obtained from the Hive command.

### Corrected Version of the Function:
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

By comparing the lowercase versions of the table name and the output from the Hive command in a case-insensitive manner, the corrected function should now pass the failing test cases and address the issue documented in GitHub.