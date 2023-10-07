To fix the bug in the `table_exists` method, we can modify the code to make it case-insensitive. We can use the `lower` method to convert both the table name and the stdout to lowercase before comparing them.

Here is the modified code:

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

This modification ensures that the comparison is case-insensitive and the test will pass even if the table names have different cases.