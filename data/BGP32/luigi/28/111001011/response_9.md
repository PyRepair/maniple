### Bug Overview:
The buggy function `table_exists` in the `HiveCommandClient` class is not handling the case sensitivity of table names correctly. The function checks if a table exists in Hive by running a command and then searching for the table name in the output. However, the comparison between the table name and the output is case-sensitive, leading to failing tests when table names are not in the expected case.

### Bug Cause:
The bug arises from the comparison of the table name with the output from the Hive command without considering case sensitivity. Since Hive is case-insensitive, the table names in the output are in a different case than the input table name causing the function to return incorrect results.

### Bug Fix Strategy:
To fix the bug, we need to ensure that the comparison between the table name and the output is case-insensitive. This can be achieved by converting both the table name and the output to lowercase before comparison. By doing so, we can match the table names regardless of their case.

### Corrected Version:
```python
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

In the corrected version, both the `table` and `stdout` are converted to lowercase before the comparison, ensuring a case-insensitive check for table existence. This modification addresses the reported bug and aligns with the suggested fix in the GitHub issue.