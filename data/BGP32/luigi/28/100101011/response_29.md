### Analysis:
1. The `table_exists` function in `hive.py` is supposed to check if a table exists in a database and handle partitions if specified.
2. The failing test `test_table_exists` checks various scenarios for table existence and partition handling.
3. The bug identified is related to case sensitivity in table existence checks, as highlighted in GitHub issue #896.
4. The bug occurs because the function compares the table name directly without considering case variations.
5. The `stdout` output from the `run_hive_cmd` function contains the table names in lowercase.

### Bug:
The bug in the current implementation is that the function does not handle case sensitivity correctly when checking for table existence.

### Fix Strategy:
To fix the bug, we need to ensure case insensitivity when comparing the table name with the stdout content.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in map(str.lower, stdout.split())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

The corrected function converts both the table name and the tables in `stdout` to lowercase before comparison, allowing for case-insensitive checks.

This corrected version should resolve the issue reported on GitHub and pass the failing tests.