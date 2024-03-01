### Analysis
The buggy function `table_exists` is not correctly checking if a table exists in a given database according to the provided parameters. The bug seems to be related to how the output from the `run_hive_cmd` function is being used to determine if the table exists.

### Bug Explanation
The bug lies in how the function is checking the output of the `run_hive_cmd` function. 
1. In the first branch of the `if` statement, when `partition` is not provided, the function is checking if the `table` string is present in the `stdout`. However, the condition `return stdout and table in stdout` does not guarantee an exact match between the table name and the output.
2. In the second branch, when `partition` is provided, the function is expecting the `stdout` to be a boolean result. Instead, it should check if the provided partition information matches the `stdout`.

### Fix Strategy
To fix the bug:
1. Update the logic in the first branch to perform an exact check for the table name in the `stdout`.
2. Update the logic in the second branch to properly check if the partition information matches the `stdout`.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                              (%s)""" % (database, table, self.partition_spec(partition)))
        return 'OK' in stdout
```

With these modifications, the function correctly checks if the table exists based on the provided parameters and returns the expected boolean values.