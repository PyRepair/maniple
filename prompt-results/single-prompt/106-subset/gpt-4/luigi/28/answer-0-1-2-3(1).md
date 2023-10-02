Based on the raised issue description, I will modify the table_exists function to be case insensitive by making both the table and stdout values lower case. Here's the fixed code snippet:

```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    # ... other methods ...

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

   # ... other methods ...
```

This should fix the bug, making the table_exists check case insensitive.