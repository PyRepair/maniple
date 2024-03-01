### Bug Explanation: 
The bug in the provided function `table_exists` lies in the condition checking for the existence of the table in the `stdout` variable. The function only checks if the `stdout` variable contains a non-empty string, which is incorrect because even a non-empty string might not contain the table name. This leads to incorrect results in the test cases, causing them to fail.

### Bug Fix Strategy:
To fix the bug, we need to modify the condition checking for the table name in the `stdout` variable. Instead of just checking for a non-empty string, we should specifically look for the existence of the table name within the `stdout` string.

### Corrected Version:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        
        return table in stdout
```

By making this adjustment, we now correctly check if the table name exists within the `stdout` string, which should resolve the issues with the failing test cases.