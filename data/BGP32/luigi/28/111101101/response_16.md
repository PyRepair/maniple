### Bug Explanation
The bug in the `table_exists` function arises from the way the return value of the `run_hive_cmd` function is being processed. The function checks if the table name is present in the output of `run_hive_cmd` to determine if the table exists. However, in the case where the table name is part of another string in the output, the function incorrectly concludes that the table exists.

### Bug Fix Strategy
To fix the bug, we need to modify the condition checking logic to ensure that the table name is a standalone word in the output string.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout.split()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
    
        if stdout:
            return True
        else:
            return False
```

By splitting the `stdout` string into words using `split()`, we ensure that we are checking for the presence of the table name as a separate entity, which resolves the bug.