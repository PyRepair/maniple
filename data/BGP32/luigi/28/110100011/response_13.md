The buggy function `table_exists` in the `HiveCommandClient` class is not handling case sensitivity correctly when checking for the existence of a table in the Hive database. This is causing the failing test cases in `hive_test.py` to fail when checking for table existence.

The issue originates from the comparison between the table name and the stdout of the Hive command. The table name should be converted to lowercase before comparison to make it case insensitive.

To fix this bug:
1. Modify the code to convert the `table` variable to lowercase before checking if it exists in the `stdout`.
2. Update the function to use the lowercased table name for comparison with the `stdout`.
3. This change will ensure that the table existence check is case insensitive.

Here is the corrected version of the `table_exists` function:

```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

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

With this correction, the `table_exists` function will now handle case insensitivity correctly, and the failing test cases should pass.