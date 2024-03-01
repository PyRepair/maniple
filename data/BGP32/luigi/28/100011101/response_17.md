### Bug Explanation
The bug in the `table_exists` function is due to the comparisons made on the `stdout` variable. The function returns `stdout and table in stdout`, which checks if `stdout` is not empty and if `table` is a substring of `stdout`. However, in some cases (e.g., when the `table` is part of a longer string in `stdout`), this comparison doesn't work correctly.

Additionally, the function's logic for the `else` case when a partition is provided seems to be incomplete, as it only checks if `stdout` is not empty but doesn't check for the specific partition.

### Fix Strategy
To fix the bug, we need to modify the logic of the function to properly handle the check for table existence based on the `stdout` output. Additionally, we need to ensure that the function correctly checks for the specific partition when provided.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout.split('\n')

    else:
        partitions = run_hive_cmd(
            """use {0}; show partitions {1} partition ({2})""".format(
                database, table, self.partition_spec(partition)
            )
        )
        return any(partition in partitions.split('\n') for partition in self.partition_spec(partition).values())
``` 

This corrected function properly splits the `stdout` output by newlines to check for the exact table existence and partitions when provided. It handles both cases where the table name is standalone and when it is part of other outputs in the `stdout`.