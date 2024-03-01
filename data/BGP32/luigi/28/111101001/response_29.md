The bug in the provided function `table_exists` lies in the comparison of the table name with the output of the `run_hive_cmd` function. The current implementation checks if the table name is present in the entire stdout string, which is causing the incorrect behavior.

To fix the bug, we need to modify the comparison logic to only check if the exact table name is present in the returned stdout string.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        
        if stdout:
            return True
        else:
            return False
```

By splitting the stdout string on '\n' before performing the check, we ensure that only the exact table names are considered for existence. This change should make the function pass the failing test cases.