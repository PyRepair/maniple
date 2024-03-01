### Explanation of the bug

The bug in the `table_exists` function lies in the comparison of the table name with the stdout output from the `run_hive_cmd` function. The function is expecting the table name to match exactly with the stdout output, but it fails to handle cases where the case of the table names is different.

### Strategy for fixing the bug

To fix the bug, we need to modify the comparison between the table name and the stdout output to be case-insensitive. This way, we can correctly determine if the table exists regardless of the case of the table name.

### Corrected version of the function

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and table.lower() in map(str.lower, stdout.split())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

In the corrected version, we convert both the table name and the output from `run_hive_cmd` to lowercase using `lower()` and then use the `in` operator to check if the table exists in the stdout output. This modification allows for a case-insensitive comparison.