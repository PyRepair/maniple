### Bug Explanation
The bug in the `table_exists` function arises from the comparison logic in the `if` conditions. In the first part of the function, when `partition` is None, the function checks if the `table` name is present in the `stdout`. However, the comparison `table in stdout` does not handle cases where the table name is surrounded by other characters, as seen in the failing tests where `OK\nmytable` is considered a match.

In the second part of the function, when `partition` is not None, the function tries to find the specified partition using `show partitions`, but the comparison of `stdout` to determine existence is not handled correctly, leading to incorrect return values and failing tests.

### Fix Strategy
To fix the bug, we need to adjust the comparison logic to clearly check for the exact presence of the table name in the `stdout`. We should also ensure the correct handling of partition checks and comparisons with `stdout`.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
    
        return stdout.strip() != ''
```

In the corrected version:
- We split `stdout` by newline characters to get individual table names when checking for table existence.
- We use `.strip()` to remove leading and trailing whitespace and check if the `stdout` is not empty to determine partition existence.
- These adjustments ensure accurate comparisons for table and partition existence checks, addressing the bug in the original function.