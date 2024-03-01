The bug in the `table_exists` function is caused by the way the function checks for the existence of a table in the output of the `run_hive_cmd` function. The function incorrectly checks if the table name is in the entire output string, leading to false positives.

To fix this bug, we should split the output string by newline characters and then check if the table name is in the list of lines.

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

With this correction, the function will split the output by newline characters and then check if the table name is present in the list of lines, giving the correct behavior for the function.

This corrected version should pass the failing test cases provided.