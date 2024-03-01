The bug in the `table_exists` function arises from the case sensitivity when checking if a table exists in Hive. The function performs a direct comparison between the provided table name and the output of the Hive command, which can lead to failures due to case differences.

To fix this bug, we need to convert both the table name and the output from Hive command to lowercase before comparison. This way, we ensure case insensitivity in the check for table existence.

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

In the corrected version, both `table` and `stdout` variables are converted to lowercase using the `lower()` method before comparison. This adjustment ensures that the comparison is not affected by the cases of the strings and resolves the issue of table existence being case sensitive.

By making this change, the function now fulfills the expected behavior of being case insensitive when checking for the existence of tables in Hive.