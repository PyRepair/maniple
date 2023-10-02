To fix the bug in the `table_exists` method, we can modify the code to make it case-insensitive by comparing the lowercase versions of the table name and the output from Hive.

Here's the updated code:

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

Now, the comparison `table.lower() in stdout.lower()` ensures that the table name is matched in a case-insensitive manner.

Please note that this fix assumes that the output from Hive is in lowercase. If it's not the case, you may need to modify the code accordingly.