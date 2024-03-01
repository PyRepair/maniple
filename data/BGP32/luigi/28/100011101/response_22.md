### Bug Explanation
The bug in the `table_exists` function lies in the condition check when determining if a table exists in the database. The function compares the table name to the output received from the `run_hive_cmd` function, but there is an issue with how the comparison is being made. The function expects the entire table name to be in the output, while the output may contain additional information like column names or row counts that could cause the comparison to fail.

### Bug Fix Strategy
To fix the bug, we need to modify the comparison logic to ensure that only the exact table name is checked in the output. One way to approach this is to split the `stdout` output by line breaks and compare each line separately against the table name.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        
        return any(table in line for line in stdout.split('\n'))
```

By splitting the `stdout` output by line breaks and checking each line separately against the table name, we can accurately determine if the table exists in the database. This corrected version of the function should pass the failing tests and provide the expected output.