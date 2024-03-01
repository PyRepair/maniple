The bug in the function `table_exists` is caused by a case sensitivity issue in comparing table names between the input and the output from the `run_hive_cmd` function. The function needs to be modified to compare the table names in a case-insensitive manner to align with the behavior of Hive, which is case insensitive.

Here is the corrected version of the function:

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

By converting both the `table` and `stdout` to lowercase before comparison, the function now performs a case-insensitive check for the existence of the table.

This correction addresses the issue raised in GitHub and ensures that the test cases with different table cases (e.g., 'mytable' vs. 'MyTable') will pass.