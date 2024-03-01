## Analysis

The buggy function `table_exists` is not performing case-insensitive check when comparing the table names in the stdout returned from the `run_hive_cmd` function. This leads to failing tests where table names with different cases are not being recognized as existing tables. The issue was reported on GitHub as #896, suggesting that the function should be case insensitive.

### Error Location
The error lies in the comparison of the table name with the output from `run_hive_cmd`.

### Cause of the Bug
The bug occurs because the function does a direct comparison of the table name with the stdout without considering case sensitivity. Hive is case insensitive, and table names are usually returned in lowercase, leading to failed comparisons when using table names with different cases.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the function to perform a case-insensitive comparison by converting both the `table` and the data in `stdout` to lowercase before comparison.

## Corrected Version

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

In the corrected version, both the `table` name and the `stdout` data are converted to lowercase before comparison using `lower()`. This ensures that the comparison is case insensitive, fixing the bug reported in the failing tests.