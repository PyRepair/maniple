The buggy function `table_exists` in `luigi/contrib/hive.py` is not handling case sensitivity correctly when checking for table existence. The function needs to compare the table name in a case-insensitive manner.

### Bug Explanation:
The bug occurs because the function compares the table name directly with the output from `run_hive_cmd()`, which can vary due to case sensitivity issues in the table name. As mentioned in the GitHub issue, Hive is case-insensitive, so the comparison should also be case-insensitive.

### Bug Location:
The bug is in the line:
```python
return stdout and table in stdout
```
and
```python
return stdout and table in stdout.lower()
```

### Fix Strategy:
To fix the bug, we need to convert both the table name and the output from `run_hive_cmd()` to lowercase before comparison.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd(f'use {database}; show partitions {table} partition ({self.partition_spec(partition)})')
        return bool(stdout)
```

In this corrected version:
- Both `table` and `stdout` are converted to lowercase using the `lower()` method before comparison.
- The function now returns `True` if `stdout` is not empty.

By implementing the above fix, the `table_exists` function should now pass all the test cases provided.