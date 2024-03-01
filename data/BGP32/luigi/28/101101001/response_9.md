### Bug Explanation
The buggy function `table_exists` is failing the test cases due to a logic error in the conditional check for table existence. The function checks if the table name is in the output of the `run_hive_cmd` function call. However, the check is not case-insensitive, which causes the function to fail the test cases where the table name is in a different case.

### Bug Fix Strategy
To fix the bug, we need to modify the conditional check to be case-insensitive when checking if the table name exists in the output of the `run_hive_cmd` function call.

### Corrected Function
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table.lower() in map(str.lower, stdout.split())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
    
        if stdout:
            return True
        else:
            return False
```

By converting both the table name and the output of `run_hive_cmd` to lowercase when checking table existence, we ensure that the check is case-insensitive and the function will pass the failing test cases.