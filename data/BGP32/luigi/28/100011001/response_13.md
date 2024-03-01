### Bug Explanation
The bug in the `table_exists` function is caused by the condition checking for the existence of the table. When the function receives the stdout from the `run_hive_cmd` function, it checks if the table name exists in the stdout. However, the check is failing in some cases because of the formatting of the stdout. The function is not properly handling the case where the table name is in a new line after the 'OK' response. This causes the condition to fail even when the table actually exists.

### Bug Fixing Strategy
To fix the bug, we need to modify how we check for the existence of the table in the output from the `run_hive_cmd` function. We should split the stdout into lines and then check each line for the presence of the table name. This way, we can handle cases where the table name is on a new line.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return stdout is not None
```

By splitting the stdout into lines using `split('\n')` before checking for table existence, we ensure that the function can correctly handle multiple lines of output and properly identify the existence of the table name. This corrected version should pass the failing tests.