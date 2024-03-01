### Bug Explanation
The bug in the `table_exists` function is due to the condition `return stdout and table in stdout` in the first part of the if statement. The logic here is flawed as it only checks if `table` is in `stdout`, but it should be checking if the whole line containing the table name exists in `stdout` without any text manipulation. This issue causes incorrect evaluation and leads to the failing test cases.

### Fix Strategy
To fix the bug, we need to modify the condition checking in the first part of the if statement to ensure that the whole line containing the table name is present in the `stdout` output from the query. This adjustment will provide the correct matching criteria and make the function return the expected result.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.splitlines()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

By splitting the `stdout` into lines and checking if the whole line with the table name exists in the output, we address the bug and ensure the correct behavior of the `table_exists` function.