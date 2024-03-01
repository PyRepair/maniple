### Bug Explanation
The bug in the `table_exists` function lies in the comparison logic when checking if the table exists in the Hive database. The function is returning the result based on whether `stdout` contains the table name as a substring. This approach is problematic because the `stdout` may contain multiple tables or characters around the table name, leading to incorrect results.

### Fix Strategy
To fix this bug, we need to modify the comparison logic to ensure that the exact table name is present in the `stdout` output. This can be achieved by splitting the `stdout` by newline characters and then checking if the table name exactly matches any of the lines.

### Corrected Code
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

Now, the function will split the `stdout` by newline characters and check if the exact table name exists in the output. This modification ensures that the function accurately determines whether the table exists in the Hive database.