The bug in the provided function is originating from the condition `return stdout and table in stdout` in the first part of the `if` statement. This condition does not accurately check if the table exists in the output from the `run_hive_cmd` function. Instead, it evaluates to `True` if `stdout` is not empty, irrespective of whether the table exists in it or not.

To fix this bug, we need to modify the condition to check if the table name is exactly present in the `stdout`. 

Here is the corrected version of the function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return table in stdout.splitlines()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

This corrected version first splits the `stdout` by lines and checks if the table name is specifically present in the output.

With this fix, the function should now pass the failing test cases provided.