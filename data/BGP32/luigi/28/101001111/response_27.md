### Bug Explanation
The bug in the `table_exists` function arises from a case sensitivity issue when checking for table existence in Hive. The function compares the table name provided in the parameter with the table names retrieved from Hive, but Hive returns table names in lowercase, causing the comparison to fail for capitalized table names.

### Bug Fix Strategy
To fix the bug, we need to ensure that the comparison between the provided table name and the table names retrieved from Hive is case-insensitive. One way to achieve this is by converting both the provided table name and the retrieved table names to lowercase before comparison.

### Corrected Version of the Function
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

### Impact of the Fix
The corrected version of the `table_exists` function will ensure that the comparison between the table names is case-insensitive, addressing the issue raised in the GitHub report. Now, the function will correctly detect the existence of tables regardless of case discrepancies.