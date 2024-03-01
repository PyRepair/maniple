### Bug Explanation:
The bug in the `table_exists` function lies in the conditional check where it returns True if the string `stdout` is not empty, regardless of whether the `table` exists in `stdout`. This causes the test cases to fail because the function doesn't accurately determine if the table exists in the output of the `run_hive_cmd` function.

### Fix Strategy:
To fix this bug, we need to modify the conditional check to verify if the table name is present in the `stdout` output when checking for table existence. We should also handle cases where the table name may appear in multiple lines in the output.

### Corrected Version of the `table_exists` function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                              (%s)""" % (database, table, self.partition_spec(partition)))
    
        return True if stdout else False
```

By splitting the `stdout` output by newline characters and checking if the `table` exists in any of those lines, we ensure a more accurate determination of table existence, fixing the bug and making the function behave correctly for all test cases.