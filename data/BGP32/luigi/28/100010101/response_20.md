### Analysis
The buggy function `table_exists` is not properly checking for the existence of a table in the database. In the first part of the function, when `partition` is `None`, it searches for the table with `show tables` but does not return the correct output format. In the second part, when a `partition` is provided, it does not properly form the `show partitions` command string. This leads to incorrect checking of table existence, causing the test cases to fail.

### Bug
1. In the first part of the function, the output format from `show tables` is not handled correctly.
2. In the second part of the function, the `show partitions` command string is not properly formatted.

### Fix
1. Modify the output parsing logic when using `show tables` to check for table existence properly.
2. Correct the formatting of the `show partitions` command when a partition is provided to check for its existence.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables'.format(database))

        return stdout and table in stdout.split("\n")
    else:
        partition_str = ', '.join(["{0}='{1}'".format(k, v) for k, v in partition.items()])
        stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2});'.format(database, table, partition_str))

        return bool(stdout)
```

This corrected version properly handles the output from `show tables` by splitting it on newlines, and correctly formats the `show partitions` command string when a partition is provided. This should pass all the failing test cases.