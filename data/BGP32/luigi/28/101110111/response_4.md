To fix the bug in the `table_exists` function, we need to make the comparison between the `table` name and the tables in the `stdout` case insensitive. This will allow the function to correctly identify tables regardless of the case. Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in map(str.lower, stdout.split('\n') if stdout else [])
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

In this corrected version:
- We use `table.lower()` to convert the table name to lowercase for case insensitivity.
- We use `map(str.lower, stdout.split('\n') if stdout else [])` to convert all the table names in `stdout` to lowercase for case insensitivity in both cases where `stdout` is not empty.
- We then check if the lowercase table name is in the list of lowercase table names in `stdout`.

With this correction, the function will now correctly handle case sensitivity and pass all the test cases mentioned above.