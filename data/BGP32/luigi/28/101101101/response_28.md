### Bug Explanation:
The bug in the `table_exists` function lies in the logic used to check for the existence of a table in the Hive database. The issue arises from how the function handles the stdout value returned from the `run_hive_cmd` function. The function incorrectly checks if the table name is directly in the stdout string instead of split by newlines.

### Bug Fix Strategy:
To fix the bug, we need to modify the logic used to check if the table exists in the stdout string. Instead of directly checking if the table name is in the stdout string, we should split the stdout string by newlines and then check if the table name exists in any of the resulting lines.

### Corrected Function:
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

By making the above changes to the `table_exists` function, the corrected version should now pass all the failing test cases and satisfy the expected input/output values.