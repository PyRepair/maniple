To address the bug in the `table_exists` function and make it case insensitive, we need to modify the function to compare table names in a case-insensitive manner. 

Here is the corrected version of the `table_exists` function:

```python
# The relative path of the buggy file: luigi/contrib/hive.py

# The corrected version of the buggy function
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

In this corrected version, we modify the comparison to `table.lower() in map(str.lower, stdout.split())` to make it case insensitive. This change will ensure that the table name comparison is done in a way that ignores case discrepancies.

By making this adjustment, the `table_exists` function should now pass the failing test cases and address the issue raised on GitHub related to case sensitivity in table existence checks.