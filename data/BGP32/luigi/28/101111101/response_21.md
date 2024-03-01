## Bug Explanation
The bug in the `table_exists` function occurs because the `run_hive_cmd` method is returning the correct output but the function is not correctly processing the response. The function checks if the table name is present in the output string but does not handle multiple lines in the output where the table name may appear. This causes the function to sometimes return incorrect results, failing the test cases.

## Bug Fix Strategy
To fix the bug, we need to modify the logic of how we check if the table exists in the output of the `run_hive_cmd` function. We should split the output by newline characters and check if the table name exists in any of the lines. By doing so, we will correctly identify if the table exists in the database.

## Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split('\n')
    else:
        partition_spec = self.partition_spec(partition)
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition ({2})""".format(database, table, partition_spec))

        return bool(stdout)
```

By splitting the `stdout` by newline characters and checking if the table name exists in any of the lines returned by `run_hive_cmd`, we ensure that we capture the correct table presence in the database. This corrected version of the function should now pass the failing test cases.