### Bugs identified in the buggy function
1. The `table_exists` function does not handle case insensitivity properly when checking if a table exists.
2. The function does not correctly check if the table exists based on the output of the `run_hive_cmd` function.

### Bug causes
1. In the failing test where `table = 'mytable'` and the `stdout = 'OK'`, the function fails because it expects `'mytable'` to be present in `stdout` when the `run_hive_cmd` function only returns `'OK'`. This causes the function to return `False` incorrectly.
2. In the failing test where `table = 'MyTable'` and the `stdout = 'OK\nmytable'`, the function also fails due to case insensitivity. The function should consider case sensitivity when checking if the table exists.

### Bug-fix strategy
1. Modify the `table_exists` function to handle case insensitivity properly when checking for the existence of a table.
2. Update the logic to correctly check if the table exists based on the `stdout` returned by the `run_hive_cmd` function.

### Corrected version of the `table_exists` function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table.lower() in [t.lower() for t in stdout.split("\n") if t]
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition
                            ({2})""".format(database, table, self.partition_spec(partition)))
    
        return bool(stdout)
``` 

By modifying the function to handle case insensitivity when checking for table existence and updating the logic to correctly check the presence of the table in the `stdout`, the corrected version should pass the failing test cases.