### Bug Explanation:
The bug in the `table_exists` function arises from the comparison of the `table` variable with the `stdout` variable. When checking if the table exists, the function checks if the `table` value is directly included in the `stdout` value, which may cause unexpected behavior due to case sensitivity and the presence of additional information in the `stdout`.

### Bug Fix:
To fix the bug, the comparison should be made case-insensitive, and only the exact table name should be checked within the `stdout`. Additionally, the presence of newlines in the `stdout` should be accounted for to accurately determine the existence of the table.

### Corrected Version:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in map(str.lower, stdout.splitlines())
    else:
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2})".format(database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

This corrected version ensures case-insensitive comparison and accounts for newlines in the `stdout` when checking for the existence of the table.