### Buggy Function Analysis
The `table_exists` function in the `HiveCommandClient` class is designed to check if a table exists in a specific database. The function constructs a Hive command based on the input parameters and runs it using the `run_hive_cmd` function. The bug seems to be related to how the function checks the existence of the table based on the `stdout` output of the Hive command.

### Bug Identification
The bug occurs due to how the function evaluates the `stdout` variable to determine if the table exists. In the first case, when `stdout` is `'OK'`, the function incorrectly returns `True`, indicating that the table exists. This behavior is incorrect because 'OK' does not imply that the table exists. Similarly, in the second case, when the table name is different in the `stdout` than the input table name, the function still returns `True`.

### Bug Cause
The bug is caused by the function assuming the presence of any string in the `stdout` indicates the existence of the table. This assumption leads to false positives where arbitrary strings like 'OK' incorrectly trigger the table existence condition.

### Bug Fix Strategy
To fix the bug, the function should explicitly check if the table name exists in the output. Additionally, it should also handle cases where the table name is not an exact match. The function should return `True` only if the table name is an exact match in the `stdout`.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        return table in stdout.split('\n')
```

In the corrected version, the function splits the `stdout` by newlines and then checks if the `table` is present in any of the lines. This modification ensures that the function correctly identifies the existence of the table based on an exact match in the output.