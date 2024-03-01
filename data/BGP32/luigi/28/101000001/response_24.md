The bug in the provided function `table_exists` lies in the way the `run_hive_cmd` function is being called with formatted strings. 

The issue arises because the formatting of the query string for the Hive command is different in the two branches of the `if` statement. In the first branch, the query is formatted using the `format` method, while in the else branch, the query is formatted differently using the modulo operator `%`. This inconsistency can lead to incorrect command formation, causing the function to fail.

To fix this bug, we need to ensure consistent string formatting in both branches of the `if` statement. One approach is to use the `format` method for string interpolation in both cases. 

Here is the corrected version of the function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout
    else:
        spec = self.partition_spec(partition)
        stdout = run_hive_cmd('use {}; show partitions {} partition ({});'.format(database, table, spec))
    
        return bool(stdout)
```

By maintaining a consistent formatting approach using the `format` method in the corrected function, we ensure that the Hive command is properly constructed and executed, fixing the bug.