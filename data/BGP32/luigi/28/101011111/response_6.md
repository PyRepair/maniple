To fix the bug in the `table_exists` function, we need to address the case sensitivity of the table names when checking for their existence in Hive. The current implementation does not account for case differences, leading to test failures when comparing table names.

The strategy to fix this bug is to convert both the table name and the output from Hive to lowercase for comparison. This will make the `table_exists` function case-insensitive and prevent failures due to mismatching cases.

Here is the corrected version of the `table_exists` function:

```python
# The corrected version of the buggy function
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

With this correction, the `table_exists` function will compare the lowercase version of both the table name and the output from Hive, ensuring that the function is case insensitive when checking for table existence.

This fix aligns with the GitHub issue raised (#896) regarding making the `table_exists` function case insensitive.