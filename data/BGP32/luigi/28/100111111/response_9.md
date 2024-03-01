### Bug Explanation:

The bug in the `table_exists` function arises from the fact that the comparison between the table name and the tables listed in the `stdout` is case sensitive. This causes the test cases to fail when the table names have different casings. The expected behavior is for the comparison to be case insensitive.

In the failing test cases, the expected behavior is that the function should return `True` when checking for the existence of a table, regardless of the casing used in the table name.

### Bug Fix Strategy:

To fix the bug, the comparison between the table names in `stdout` and the input table name should be made case insensitive. This can be achieved by converting both the table name and the entries in `stdout` to lowercase before comparison.

### Corrected Version of the Function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
        tables = stdout.lower().split('\n')

        return table.lower() in tables
    else:
        stdout = run_hive_cmd('use {0}; show partitions {1}'.format(database, table))
        partitions = stdout.lower().split('\n')

        return self.partition_spec(partition).lower() in partitions
```

### Impact of the Fix:

By making the comparison case insensitive, the corrected `table_exists` function will now correctly return `True` when checking for the existence of a table, regardless of the casing used in the table name. This fix aligns with the expected behavior and resolves the failing test cases.