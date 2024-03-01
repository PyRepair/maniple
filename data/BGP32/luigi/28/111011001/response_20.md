### Bug Explanation:
The bug occurs because the `table_exists` function is not correctly checking for the existence of the table in the output obtained from the `run_hive_cmd` function. The function is currently checking if the table name is present in the entire output string, which leads to incorrect results.

### Bug Fix Strategy:
To fix the bug, the `table_exists` function should parse the output from `run_hive_cmd` to accurately determine if the table exists. It should not only check if the table name is present in the output but specifically look for a line that matches the table name.

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout and table + "\n" in stdout
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
    
            return bool(stdout)
```

With this correction, the function now accurately checks if the table name is present in the output from `run_hive_cmd` rather than just checking if it exists anywhere in the string. This should resolve the failing tests and ensure the function behaves as expected.