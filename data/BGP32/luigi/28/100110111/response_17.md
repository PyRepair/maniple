The bug in the `table_exists` function arises due to the case sensitivity of table names in the comparison between the table name and the output from Hive. To fix the bug and make the comparison case insensitive, we need to convert both the table name and the output to lowercase before comparing them.

Here is the corrected version of the function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

This corrected version will convert both the table name and the output to lowercase before making the comparison. This change ensures that the function is case insensitive when checking for the existence of a table in Hive.

By implementing this change, the function will pass the failing test cases provided and also address the issue raised in the GitHub thread regarding making `table_exists` case insensitive.