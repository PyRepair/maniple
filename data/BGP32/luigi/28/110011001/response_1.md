### Bug Explanation
The bug in the `table_exists` function is caused by the condition checking for the presence of the table name in the `stdout`. When checking if the table exists in the output, the function incorrectly uses a non-empty `stdout` as the condition for existence, leading to incorrect evaluations. Additionally, the else branch always returns `False` regardless of the content in `stdout`, which is incorrect behavior.

### Bug Fix Strategy
To fix the bug, we need to modify the conditions for checking if the table exists in the `stdout`. We should properly handle the cases where the table name might be present in the output string. We can also simplify the function's logic to have clearer return values based on the existence of the table in the `stdout`.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return table in stdout.split("\n")

    stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2});".format(database, table, self.partition_spec(partition)))
    return stdout.strip() != ""
```

By splitting the `stdout` and checking for table existence in the corrected version, we address the issue of incorrect condition checking. Additionally, we ensure that the function returns the correct boolean value based on the table's presence in the `stdout`.