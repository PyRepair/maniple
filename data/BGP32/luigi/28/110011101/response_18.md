### Bug Explanation
The bug in the `table_exists` function arises from the logic used to determine if a table exists based on the output of the `run_hive_cmd` function. The issue lies in the comparison of the returned value from `run_hive_cmd` to the table name. In cases where the table name is part of a larger string in the output, the function fails to correctly identify if the table exists.

The erroneous logic inside the function is causing it to return incorrect results for some cases, leading to failed assertions in the test cases.

### Bug Fix Strategy
To fix this bug, we need to adjust the comparison logic to properly check if the table name is in the output string. This adjustment will ensure that the function accurately determines if the table exists in the specified database.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition
                                ({2})""".format(database, table, self.partition_spec(partition)))
    
        return True if table in stdout else False
```

By using the `in` keyword to check if the table name is present in the `stdout` string, we ensure that the function correctly identifies the existence of the table. This corrected version should now pass the failing test cases and provide the expected output.