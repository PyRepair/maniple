### Bug Explanation
The bug in the `table_exists` function lies in the comparison logic. The function checks if the `stdout` variable contains the table name, but it does not handle cases where the table name is part of a larger string. This leads to incorrect evaluation of the presence of the table in the output of the command.

### Bug Fix Strategy
To fix the bug, we need to modify the comparison logic to check if the table name is present as a separate word in the `stdout` variable, considering it as a standalone entity.

### Corrected Version of the Function
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

With this fix, the function will split the `stdout` variable by newlines and check if the table name exists as a separate word in the output. This should ensure correct evaluation of the table existence and the function should pass the failing tests.