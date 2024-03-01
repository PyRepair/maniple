### Identified Bug:
The bug in the `table_exists` function is that it is not handling case sensitivity correctly. The function checks for the exact match between the provided table name and the tables in the Hive database without considering case differences. This leads to test failures when the case of the table names differs.

### Root Cause:
The root cause of the bug is that the function compares the table name directly with the tables returned by the Hive command `show tables`. Since Hive is case-insensitive, the table names may be returned in lowercase, causing the comparison to fail for tables with different cases.

### Strategy for Fixing the Bug:
To fix the bug and make the `table_exists` function case-insensitive, we need to convert both the table name and the tables returned by Hive to lowercase before comparison. This adjustment will ensure that the function correctly identifies the existence of a table regardless of the case used in the table name.

### Corrected Version of the `table_exists` Function:
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

In the corrected version:
- Before comparing the table name, `table.lower()` converts the provided table name to lowercase.
- `map(str.lower, stdout.split())` converts all tables returned by Hive to lowercase before checking if the lowercase table name exists in the list.
- This change ensures a case-insensitive check for table existence in the Hive database.

By making these adjustments, the `table_exists` function will now handle case sensitivity correctly and address the issue reported on GitHub regarding case-insensitive table checks.