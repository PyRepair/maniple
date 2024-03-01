To fix the bug in the `table_exists` function, we need to make it case insensitive when checking if a table exists. This can be achieved by converting the table name and the output to lowercase before comparing them.

Here is the corrected version of the `table_exists` function:

```python
class HiveCommandClient(HiveClient):
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

By converting both the `table` and `stdout` to lowercase before comparing, we ensure that the function is now case insensitive when checking for table existence.

This correction addresses the failing test cases that expected case-insensitivity when checking for table existence in Hive.