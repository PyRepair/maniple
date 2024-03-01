### Analysis
The buggy function `table_exists` checks if a table exists in a database. The bug seems to be related to the condition checking whether the table is present in the output obtained from running hive commands.

### Identified Issue
1. The bug seems to be in the condition check for `stdout`, where it only returns `True` if some output is present (not an empty string).
2. In the case where the table exists, the function should return `True`, but it is returning `True` only if some output is present, leading to the failing test cases.

### Correction Strategy
To fix the bug:
- Update the condition check for `stdout` to ensure that it explicitly checks if the table is present in the output.
- Adjust the return statements to return `True` only if the table is found in the output.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return table in stdout  # Check directly if the table is present

    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
        return table in stdout  # Check directly if the table is present
```

By making these changes, the corrected function should now pass the failing test cases.