## Fixing the buggy function

### Analysis:
1. The `table_exists` function in the `HiveCommandClient` class is supposed to check if a table exists in a specified database. It uses the `run_hive_cmd` function to run Hive commands.
2. The bug occurs due to a case-sensitivity issue when checking for table existence. The function does not consider case differences between the table name and the actual table in Hive.
3. The failing test case provided in the `hive_test.py` file exposes this bug by testing for table existence with different cases.
4. The GitHub issue highlights the need to make the `table_exists` function case-insensitive in checking for table existence.

### Bug Fix Strategy:
1. Modify the `table_exists` function to convert both the table name and the output from `run_hive_cmd` to lowercase before comparison.
2. This ensures that the comparison is case-insensitive and resolves the issue highlighted in the failing test and GitHub issue.

### Corrected Version of the `table_exists` function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

### Changes Made:
1. Modified the conditions to convert both the `table` and `stdout` values to lowercase for case-insensitive comparison.
2. Used `table.lower() in stdout.lower()` to check if the lowercase table name exists in the lowercase result from `run_hive_cmd`.

By making these changes, the corrected version of the `table_exists` function should pass the failing test case and address the case sensitivity issue highlighted in the GitHub issue.