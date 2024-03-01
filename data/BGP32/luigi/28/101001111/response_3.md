The buggy function `table_exists` in the `HiveCommandClient` class of the file `luigi/contrib/hive.py` has a bug related to case sensitivity when checking for table existence in Hive. The function compares the table name directly with the output from Hive, which can differ in case due to Hive being case-insensitive. This causes the function to incorrectly determine table existence in certain cases.

To fix the bug, we need to modify the comparison to be case insensitive. We can convert both the table name and the output from Hive to lowercase before comparison.

Here is the corrected version of the `table_exists` function:

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

This correction ensures that both the table name and the Hive output are converted to lowercase before the comparison, resolving the case sensitivity issue.

With this fix, the function will now correctly determine table existence in a case-insensitive manner, consistent with Hive behavior. This addresses the GitHub issue related to making `table_exists` case insensitive (#896).