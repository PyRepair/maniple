The bug in the provided function is that the condition for checking if a table exists is not properly implemented. In the first case, the returned stdout is only `'OK'`, which should not confirm the existence of the table 'mytable'. The function is erroneously checking for table name in the exact stdout string.

To fix this bug, we need to modify the condition to check if the table name is present within the stdout regardless of its position or other content. We can achieve this by using a more robust string matching method like splitting the stdout string and then checking for the table name within it.

Here is the corrected version of the function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))

        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

With this correction, the function will split the output by newline character and then check if the expected table name is present in the list of tables. This will fix the issue of incorrect evaluation of table existence.