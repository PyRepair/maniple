### Bug Analysis:
The bug arises from the `table_exists` function not being case insensitive when checking for the existence of tables in Hive. Specifically, the function compares the table name directly with the tables listed in stdout, leading to failures when table names are different only in case.

### Bug Location:
The buggy behavior originates from the direct comparison between the table name provided and the tables listed in the Hive output (`stdout`).

### Bug Cause:
The bug is caused by a case-sensitive string comparison between the `table` name and the tables listed in `stdout`. This leads to failures when the table names have different cases.

### Bug Fix Strategy:
To fix the bug, the comparison between the table names should be case insensitive. By converting both the `table` name and the tables listed in `stdout` to the same case (e.g., lowercase) before comparison, the function will be able to correctly identify the existence of tables without being affected by case differences.

### Corrected Version of the Function:
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

By converting both the `table` name and the entries in `stdout` to lowercase before comparison, the corrected version of the function ensures a case-insensitive check for table existence.

This corrected version should address the issue reported on GitHub (#896) and make the `table_exists` function case insensitive when verifying the existence of tables in Hive.