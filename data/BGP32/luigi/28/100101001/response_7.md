### Bug Analysis
The bug in the `table_exists` function lies in the logic to determine if the table exists based on the output received from running a Hive command. In the case where the table exists, the function should return `True`, but the current implementation checks if `stdout` is not empty to determine existence.

### Bug Cause
1. In Case 1 and Case 3, the `stdout` only contains `'OK'`, which is causing the function to return `False` even though the table actually exists.
2. In Case 2 and Case 4, the `stdout` contains multiple lines including the table name, but the function only checks if the table name is in the `stdout`, resulting in an incorrect return value.

### Fix Strategy
To fix this bug, we need to update the logic in the `table_exists` function to accurately detect whether the table exists based on the output received from the Hive command.

### Corrected Code
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout.split('\n')

    stdout = run_hive_cmd("""use %s; show partitions %s partition
                      (%s)""" % (database, table, self.partition_spec(partition)))

    return stdout is not None
```

By splitting the `stdout` on `\n` lines, we can accurately check if the table name exists in the output. Additionally, checking if `stdout` is not `None` will correctly handle cases where partitions are returned.