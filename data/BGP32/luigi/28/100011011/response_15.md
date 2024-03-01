### Bug Analysis:
The buggy function `table_exists` fails to account for case sensitivity when comparing the `table` name with the table names retrieved from the `stdout`. This leads to test failures when the case of the table name in the function call doesn't match the case of the table name in the `stdout`.

### Bug Location:
The bug exists in the comparison between the `table` and the tables in the `stdout`.

### Bug Cause:
The bug occurs because the comparison between `table` and the tables in the `stdout` is case-sensitive. When the case of the `table` passed as an argument doesn't match the case of the table names in the `stdout`, the function returns incorrect results.

### Proposed Fix Strategy:
To fix this issue, we need to convert both the `table` and the table names in the `stdout` to lowercase for case-insensitive comparison.

### Corrected Function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in map(str.lower, stdout.split())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

### Correction Rationale:
- The corrected function converts the `table` parameter to lowercase before comparing with the table names in `stdout`, ensuring a case-insensitive comparison.
- The `stdout` results are split into individual table names and each name is converted to lowercase using `map(str.lower, stdout.split())`.
- This approach adheres to the proposed fix strategy, and the corrected function should now pass the failing tests and resolve the reported GitHub issue.