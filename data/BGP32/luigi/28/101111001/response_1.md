### Bug Explanation
The bug in the `table_exists` function lies in the condition checking for the existence of the table in the output of the `run_hive_cmd` function. The function checks whether the table is in the output by using `table in stdout`, which is inherently flawed when the output contains multiple tables as in the test case. This approach leads to incorrect results and failing tests.

### Bug Fix Strategy
To fix the bug, we need to modify the logic for checking the existence of the table in the output of `run_hive_cmd`. Instead of directly checking if the table name is in the output, we should split the output by newline characters and then check if the table name appears in the list of tables.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
    
        if stdout:
            return True
        else:
            return False
```

By splitting the output by newline characters, we ensure that each table name is treated separately for comparison, fixing the bug and allowing the function to pass the failing tests.